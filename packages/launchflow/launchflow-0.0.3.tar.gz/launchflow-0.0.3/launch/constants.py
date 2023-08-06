import typer

DEFAULT_SERVER = 'https://apis.launchflow.com'

ADD_READER_HELP_TEXT = 'Adds a reader to a{}'
REMOVE_READER_HELP_TEXT = 'Removes a reader from a{}'
ADD_WRITER_HELP_TEXT = 'Adds a writer to a{}'
REMOVE_WRITER_HELP_TEXT = 'Removes a writer from a{}'
GET_HELP_TEXT = 'Prints details about a{}'
NAME_HELP_TEXT = 'The name of the {}'
PERMISSION_HELP_TEST = 'The permission to perform operations on. Should be of the format: (user|serviceAccount|domain):(email|domain)'  # noqa: E501

SERVER_ADDRESS_OPTION = typer.Option(default=DEFAULT_SERVER, hidden=True)
PERMISSION_ARG = typer.Argument(...,
                                help=PERMISSION_HELP_TEST,
                                show_default=False)
