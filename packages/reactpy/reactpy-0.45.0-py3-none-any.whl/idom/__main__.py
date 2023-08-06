import click

import reactpy
from idom._console.update_html_usages import update_html_usages


@click.group()
@click.version_option(reactpy.__version__, prog_name=reactpy.__name__)
def app() -> None:
    pass


app.add_command(update_html_usages)


if __name__ == "__main__":
    app()
