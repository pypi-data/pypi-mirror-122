import typer

app = typer.Typer()


@app.callback()
def callback():
    """
    The datagrep platform CLI.
    """


@app.command()
def build():
    """
    Build...
    """
    typer.echo("Building...")


@app.command()
def deploy():
    """
    Deploy...
    """
    typer.echo("Deploying...")


@app.command()
def release():
    """
    Release...
    """
    typer.echo("Releasing...")
