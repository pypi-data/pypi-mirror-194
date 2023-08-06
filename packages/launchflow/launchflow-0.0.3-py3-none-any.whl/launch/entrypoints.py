import typer

from launch import constants
from launch import resources
from launch import utils

app = typer.Typer()


_END_POINT = 'entrypoint'
_NAME_ARG = utils.get_name_arg(_END_POINT)


@app.command(help=utils.get_help_text(_END_POINT))
def get(
    name: str = _NAME_ARG,
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    resources.get(name, endpoint=_END_POINT, server_address=server_address)


@app.command(help=utils.get_add_reader_help(_END_POINT))
def add_reader(name: str = _NAME_ARG,
               reader: str = constants.PERMISSION_ARG,
               server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.add_reader(name=name,
                         reader=reader,
                         endpoint=_END_POINT,
                         server_address=server_address)


@app.command(help=utils.get_remove_reader_help(_END_POINT))
def remove_reader(name: str = _NAME_ARG,
                  reader: str = constants.PERMISSION_ARG,
                  server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.remove_reader(name=name,
                            reader=reader,
                            endpoint=_END_POINT,
                            server_address=server_address)


@app.command(help=utils.get_add_writer_help(_END_POINT))
def add_writer(name: str = _NAME_ARG,
               writer: str = constants.PERMISSION_ARG,
               server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.add_writer(name=name,
                         writer=writer,
                         endpoint=_END_POINT,
                         server_address=server_address)


@app.command(help=utils.get_remove_writer_help(_END_POINT))
def remove_writer(name: str = _NAME_ARG,
                  writer: str = constants.PERMISSION_ARG,
                  server_address: str = constants.SERVER_ADDRESS_OPTION):
    resources.remove_writer(name=name,
                            writer=writer,
                            endpoint=_END_POINT,
                            server_address=server_address)
