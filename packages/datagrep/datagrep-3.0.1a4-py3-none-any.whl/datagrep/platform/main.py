from typing import Iterable, Optional
import typer

import click
from click import Context
from plumbum import local, FG
import plumbum


class OrderedCommands(click.Group):
    def list_commands(self, ctx: Context) -> Iterable[str]:
        return self.commands.keys()


app = typer.Typer(cls=OrderedCommands)


@app.callback()
def callback():
    """
    The datagrep platform CLI.
    """


@app.command()
def init():
    """
    Initialize...
    """
    typer.echo("Initializing...")
    try:
        multipass = local["multipass"]
        multipass["version"] & FG

    except plumbum.commands.processes.CommandNotFound:
        typer.echo("Yeah, multipass, she knows it's a multipass.")
        typer.launch(f"https://multipass.run")


@app.command()
def build():
    """
    Build...
    """
    typer.echo("Building...")


@app.command()
def deploy(
    target: Optional[str] = typer.Argument(
        "local", help="Where to deploy the platform?"
    ),
    num_worker_nodes: Optional[int] = typer.Argument(
        2, help="The number of worker nodes to create."
    ),
):
    """
    Deploy the platform to TARGET with NUM_WORKER_NODES worker nodes.
    """
    typer.echo(
        f"Deploying the platform to {target} with {num_worker_nodes} worker nodes..."
    )

    if target == "local":
        multipass = local["multipass"]

        (
            multipass[
                "launch",
                "--cloud-init",
                "cloud-config.yaml",
                "--cpus",
                "4",
                "--disk",
                "40G",
                "--mem",
                "4G",
                "--name",
                "datagrep-head",
            ]
            & FG
        )
        multipass["exec", "datagrep-head", "sudo", "ufw", "allow", "25000/tcp"] & FG

        for worker_node_i in range(num_worker_nodes):
            (
                multipass[
                    "launch",
                    "--cloud-init",
                    "cloud-config.yaml",
                    "--cpus",
                    "4",
                    "--disk",
                    "40G",
                    "--mem",
                    "4G",
                    "--name",
                    f"datagrep-worker-{worker_node_i}",
                ]
                & FG
            )
            add_node = (
                multipass["exec", "datagrep-head", "microk8s", "add-node"]
                | local["grep"]["^microk8s join"]
            )
            (
                multipass[
                    "exec", f"datagrep-worker-{worker_node_i}", add_node().split()
                ]
                & FG
            )

    else:
        raise Exception("Not implemented")


@app.command()
def release():
    """
    Release...
    """
    typer.echo("Releasing...")
