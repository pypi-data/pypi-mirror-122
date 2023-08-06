#!/usr/bin/env python3

from enum import Enum, auto
from sys import stderr
from textwrap import dedent
from time import sleep
from typing import Any, Mapping, NamedTuple, Optional, Text, Tuple, Union
from pathlib import Path

import requests

HOST = "https://api.copernic360.ai/v0.1/"


def api_route(route: Text, host: Optional[Text] = None):
    if len(route) == 0:
        raise ValueError("Expected a route")
    if route[0] == "/":
        route = route[1:]
    host = host or HOST
    return f"{host}/{route}"


def set_host(new_host):
    global HOST
    if new_host.startswith("http://"):
        new_host = new_host[len("http://") :]
    if not new_host.startswith("https://"):
        new_host = f"https://{new_host}"
    if new_host[-1] != "/":
        new_host += "/"
    if not new_host.endswith("/v0.1/"):
        new_host += "v0.1/"
    if new_host.endswith("/"):
        new_host = new_host[:-1]
    HOST = new_host


def check_health():
    from sys import stdout

    isatty = stdout.isatty()
    if isatty:
        print("Checking health...\n")
    response = requests.get(api_route("check_health"))

    raise_on_error(response)

    if isatty:
        print("\n{}\n".format(response.json()))
    else:
        print(response.json()["status"].strip())
    return response.json()


def check_login(username, password):
    print("\nChecking login details...")

    url = api_route(f"users/{username}/health")
    response = requests.get(url, auth=(str(username), str(password)))

    raise_on_error(response)

    print("\n{}\n".format(response.json()))
    return response.json()


def check_credit(username, password):
    from sys import stdout

    isatty = stdout.isatty()
    if isatty:
        print("\nChecking credit...")

    url = api_route(f"users/{username}/credit")
    response = requests.get(url, auth=(str(username), str(password)))

    raise_on_error(response)

    if isatty:
        print("\n{}\n".format(response.json()))
    else:
        print(response.json()["credit"])
    return response.json()


def change_password(username, old_password, new_password):
    print("\nChanging password...")

    url = api_route(f"users/{username}/change_password")
    headers = {"Content-Type": "application/json"}
    response = requests.patch(
        url,
        json=dict(new_password=new_password),
        auth=(str(username), str(old_password)),
        headers=headers,
    )

    raise_on_error(response)

    print("\n{}\n".format(response.json()))
    return response.json()


def generate_api_key(username, password):
    print("\nGenerating new API key...")

    url = api_route("generate_api_key")
    response = requests.patch(url, auth=(str(username), str(password)))

    raise_on_error(response)

    api_key = response.json()["api_key"]
    print(
        "\nPlease write down your API key, "
        "you won't be able to retrieve it again later:\n{}\n".format(api_key)
    )
    return response.json()


def process_content(
    credentials: Tuple[Text, Text], content_path: Union[Text, Path], config_file
):
    print("\nProcessing content...")

    signing = get_signed_url(credentials, content_path)
    if signing is not None:
        upload_content(content_path, **signing.kwargs)
        get_configuration(credentials, signing.handle, config_file)


def pay_for_content(username, password, content_handle):
    print("\nPaying for content...")

    url = api_route("pay_for_content")
    content_handle_dictionary = {"content_handle": str(content_handle)}
    response = requests.post(
        url, auth=(str(username), str(password)), json=content_handle_dictionary
    )

    raise_on_error(response)

    print("\n{}\n".format(response.json()))


def raise_on_error(response):
    if not 200 <= response.status_code < 300:
        raise ValueError(
            "\n{}\n".format(response.text)
            + "\nIf error continues contact support on <support@kagenova.com>."
        )


class SignedURL(NamedTuple):
    handle: Text
    kwargs: Mapping[Text, Any]


def get_signed_url(
    credentials: Tuple[Text, Text], content_path: Union[Text, Path]
) -> Optional[SignedURL]:
    from sys import stderr

    if Path(content_path).suffix.lower() not in {".jpg", ".jpeg", ".png", ".mp4"}:
        print("Expected an image (.jpeg, .jpg, .png) or a video (.mp4).", file=stderr)
        return None

    response = requests.post(
        api_route("register_upload"),
        auth=credentials,
        json={"filename": Path(content_path).name},
    )

    raise_on_error(response)

    json = response.json()
    signed_kwargs = dict(url=json["url"], fields=json["fields"])
    print(
        "This is your content handle, please record this for future use: {}".format(
            json["content_handle"]
        )
    )
    return SignedURL(json["content_handle"], signed_kwargs)


def upload_content(
    filepath: Union[Text, Path], url: Text, fields: Optional[Mapping[Text, Text]] = None
):
    from sys import stderr

    if fields is None:
        fields = dict()

    filepath = Path(filepath)
    with filepath.open("rb") as fileobj:
        response = requests.post(
            url, data=dict(**fields), files=dict(file=(str(filepath), fileobj))
        )

    if not (200 <= response.status_code < 300):
        print(response.status_code, file=stderr)
        print(response.content, file=stderr)

    raise_on_error(response)


def get_configuration(
    credentials: Tuple[Text, Text],
    content_handle: Text,
    config_filename: Union[Text, Path],
    format: int = 1,
):
    total_waited = 0
    wait = 3
    print("Waiting for configuration", end="", flush=True)
    status = config_status(content_handle, credentials)
    for i in range(5):
        if status != ConfigStatus.UNKNOWN:
            break
        sleep(5)
        status = config_status(content_handle, credentials)
    else:
        print(
            "Having trouble starting the configuration process.",
            file=stderr,
            flush=True,
        )
        return
    while status == ConfigStatus.RUNNING:
        sleep(wait)
        status = config_status(content_handle, credentials)
        total_waited += wait
        print(".", end="", flush=True)
    print("")
    if status != ConfigStatus.SUCCESS:
        print("Creating configuration failed", file=stderr, flush=True)
        return
    print("Retrieving configuration")

    get_configuration_url = api_route(f"contents/{content_handle}/format/{format}")

    response = requests.get(get_configuration_url, auth=credentials)

    raise_on_error(response)

    if not 200 <= response.status_code < 300:
        print(response.request.url)
        print(response.request.headers)
        print(response.request.body)
        print(response.status_code)
        print(response.content)
        raise Exception(
            "\nFile configuration failed, if this error persists contact support."
        )

    with Path(config_filename).open("wb") as config:
        config.write(response.content)
    print("\nSuccessfully uploaded and configured content. \n")


class ConfigStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()
    UNKNOWN = auto()


def config_status(content_handle: Text, credentials: Tuple[Text, Text]) -> ConfigStatus:
    url = api_route(f"contents/{content_handle}/ready")

    result = requests.get(url, auth=credentials)
    if result.status_code != 200 or result.json() is None:
        return ConfigStatus.UNKNOWN
    if "error" in result.json():
        return ConfigStatus.FAILURE
    if result.json().get("status", "").lower() == "unknown":
        return ConfigStatus.UNKNOWN
    return ConfigStatus.SUCCESS if result.json()["result"] else ConfigStatus.RUNNING


def get_contents(credentials: Tuple[Text, Text]):
    route = api_route(f"users/{credentials[0]}/contents")
    response = requests.get(route, auth=credentials)
    raise_on_error(response)
    for handle, data in response.json().items():
        print(
            dedent(
                f"""
            - handle: {handle}
              creation: {data['creation']}
              paid: {data['paid']}
            """
            ).strip(),
        )
