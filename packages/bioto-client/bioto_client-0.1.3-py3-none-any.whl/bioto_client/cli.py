from bioto_client.domain.users import User, UserException
from bioto_client.domain.auth import SessionExpired
from bioto_client.infrastructure.repository.api import HTTPException
from bioto_client.infrastructure.context import context
import functools
from rich import print
import typer

# Hide sensitive info when an exception occurs
app = typer.Typer(
    name="Bioto CLI",
    add_completion=True,
    pretty_exceptions_show_locals=False
)
user: User = None


def handle_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global user
        user = assert_session()

        try:
            func(*args, **kwargs)
        except HTTPException as error:
            print(str(error))
            raise typer.Exit(code=1)
        except SessionExpired:
            print("Session expired, please login")
            context.get_users_service().clear()
            raise typer.Exit(code=2)

    return wrapper


def assert_session() -> User:
    try:
        user = context.get_users_service().load()
    except UserException:
        print("Not logged in, please take the following steps:\n")
        user = context.get_auth_service().login()
        context.get_users_service().store(user)
        context.get_repository(user).update_user()
        print("\nSuccesfully logged in.\n")

    return user


@app.command()
@handle_request
def user():
    """
    Shows which user is logged in
    """
    print("Bioto CLI client")
    print(f"Session token ***{user.access_token[-7:]}")


@app.command()
@handle_request
def gardens():
    """
    Overview of gardens you either maintain or are subscribed to
    """
    print(context.get_repository(user).get_gardens())


@app.command()
@handle_request
def search_garden(
    query: str = typer.Argument("Bioto", help="Name of a garden")
):
    """
    Find a garden to subscribe to
    """
    print(context.get_repository(user).search_garden(query))


@app.command()
@handle_request
def subscribe_garden(
    uuid: str = typer.Argument(None, help="garden UUID")
):
    """
    Subscribe to a garden
    """
    print(context.get_repository(user).subscribe_garden(uuid))
