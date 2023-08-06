import requests

import yaml
import typer

from launch.auth import cache
from launch import constants

app = typer.Typer()


@app.command()
def get(
    name: str,
    server_address: str = typer.Option(default=constants.DEFAULT_SERVER),
):
    creds = cache.get_user_creds()
    response = requests.get(
        f'{server_address}/organization?name={name}',
        headers={'Authorization': f'Bearer: {creds.id_token}'})

    response_json = response.json()
    # TODO: we should order these in a logical order on the backend.
    print('    ' + yaml.dump(response_json).replace('\n', '\n    '))


if __name__ == "__main__":
    app()
