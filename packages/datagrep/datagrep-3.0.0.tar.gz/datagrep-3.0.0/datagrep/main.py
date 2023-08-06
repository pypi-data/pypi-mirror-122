import typer

from .platform.main import app as platform_app

app = typer.Typer()
app.add_typer(platform_app, name="platform")


@app.callback()
def callback():
    """
    The datagrep CLI.
    """
