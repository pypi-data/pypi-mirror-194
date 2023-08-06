import click

from chinaski.henry import core


@click.command()
@click.option(
    "--file",
    "file",
    type=str,
    default=None,
    help="REQUIRED - Path to single file to scan.",
    show_default=True,
)
def cli(
    file: str,
) -> None:
    """Cli entry for chinaski.

    Will call the core function and print the results found

    :param file: REQUIRED - Path to single file to scan.
    :return: None, will only print results
    """

    for result in core(file_path=file):
        print(result)
