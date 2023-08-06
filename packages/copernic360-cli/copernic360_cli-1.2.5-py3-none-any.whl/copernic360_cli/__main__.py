import click
import functools

from . import public_options


def host_option(func):
    """Allow modifying the host URL."""

    @click.option(
        "--host",
        envvar="COPERNIC360_HOST",
        help="Set copernic360 host if using a private server.",
        default=public_options.HOST,
        show_envvar=True,
        show_default=True,
    )
    def wrapper_credential_options(*args, **kwargs):
        if kwargs.get("host", None):
            public_options.set_host(kwargs.pop("host"))
        return func(*args, **kwargs)

    return wrapper_credential_options


def credential_options(func):
    """Helper to create common (but not universal) options."""

    @functools.wraps(func)
    @click.option(
        "-u",
        "--user",
        prompt=True,
        envvar="COPERNIC360_USER",
        help="Your copernic360 username.",
        show_envvar=True,
    )
    @click.option(
        "-p",
        "--password",
        prompt=True,
        hide_input=True,
        envvar="COPERNIC360_PASSWORD",
        help="Your copernic360 password. Omit this to be prompted for it.",
        show_envvar=True,
    )
    def wrapper_credential_options(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper_credential_options


@click.group()
@host_option
def cli():
    """Command-line interface for the copernic360 Cloud API.

    Commands which require credentials will first look for them in
    the environment variables COPERNIC360_USER and COPERNIC360_PASSWORD.
    Otherwise, they will prompt you for them.

    You can get detailed help for each comment by running:

    \b
    copernic360 COMMAND - -help"""


@cli.command()
def check_health():
    """Check whether the API is accessible."""
    public_options.check_health()


@cli.command()
@credential_options
def check_login(user, password):
    """Check whether your API credentials are valid."""
    public_options.check_login(user, password)


@cli.command()
@credential_options
def check_credit(user, password):
    """Check how many credits are left on your account."""
    public_options.check_credit(user, password)


# TODO: Figure out how to use our credential_options helper for this one.
@cli.command()
@click.option(
    "-u",
    "--user",
    prompt=True,
    envvar="COPERNIC360_USER",
    help="Your copernic360 username.",
    show_envvar=True,
)
@click.option(
    "-p",
    "--password",
    prompt="Old password",
    hide_input=True,
    envvar="COPERNIC360_PASSWORD",
    help="Your copernic360 password. Omit this to be prompted for it.",
    show_envvar=True,
)
@click.option(
    "--new-password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="New password for your account. Omit this to be prompted for it.",
)
def change_password(user, password, new_password):
    """Change the password for your account."""
    public_options.change_password(user, password, new_password)


@cli.command()
@credential_options
def generate_api_key(user, password):
    """Generates a new API key for your account."""
    public_options.generate_api_key(user, password)


@cli.command()
@click.argument("content_file")
@click.argument("config_file")
@credential_options
def process_content(user, password, content_file, config_file):
    """Upload content to the cloud and obtain the corresponding configuration"""
    public_options.process_content((user, password), content_file, config_file)


@cli.command()
@click.argument("content_handle")
@credential_options
def pay_for_content(user, password, content_handle):
    """Pay for content with the given content handle.

    Generally, payment (in copernic360 credits) is processed at the time content
    is uploaded, unlesss there were insufficient credits. After requesting more
    credits, this call will finish processing the content and payment.
    """
    public_options.pay_for_content(user, password, content_handle)


@cli.command()
@click.argument("content_handle")
@click.argument("config_file")
@click.option("--format", default="1", show_default=True, type=click.Choice(["1", "3"]))
@credential_options
def configuration(user, password, content_handle, config_file, format: int):
    """Obtain the configuration associated with a given content handle"""
    public_options.get_configuration(
        (user, password), content_handle, config_file, format=format
    )


@cli.command()
@credential_options
def contents(user, password):
    """List of content handles and creation dates"""
    public_options.get_contents((user, password))


if __name__ == "__main__":
    cli()
