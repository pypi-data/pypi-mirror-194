import requests

import typer
import yaml

from launch.auth import cache
from launch import constants


app = typer.Typer()


@app.command()
def get(
    name: str,
    server_address: str = constants.DEFAULT_SERVER,
):
    creds = cache.get_user_creds()
    response = requests.get(
        f'{server_address}/environment?name={name}',
        headers={'Authorization': f'Bearer: {creds.id_token}'})

    response_json = response.json()
    # TODO: we should order these in a logical order on the backend.
    print('    ' + yaml.dump(response_json).replace('\n', '\n    '))
