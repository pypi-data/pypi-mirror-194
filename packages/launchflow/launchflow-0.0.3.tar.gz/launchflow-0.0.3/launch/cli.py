import typer

from launch.auth import flow as auth_flow
from launch import constants
from launch import entrypoints
from launch import environments
from launch import flows
from launch import organizations

app = typer.Typer()

app.add_typer(entrypoints.app,
              name="entrypoint",
              help='Perform operations on an entrypoint.')
app.add_typer(environments.app,
              name="environment",
              help='Perform operations on an environment.')
app.add_typer(flows.app,
              name="flow",
              help='Perform operations on a flow.')
app.add_typer(organizations.app,
              name="organization",
              help='Perform operations on an organization.')


@app.command(help='Authenticate with launchflow.')
def auth(auth_endpoint: str = typer.Option(default=constants.DEFAULT_SERVER,
                                           hidden=True)):
    auth_flow.web_server_flow(auth_endpoint)


def main():
    app()


if __name__ == "__main__":
    main()
