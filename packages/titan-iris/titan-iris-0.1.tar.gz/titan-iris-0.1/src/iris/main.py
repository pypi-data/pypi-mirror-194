"""
This is the main file for the sdk cli. It is responsible for handling the cli commands and passing them to the sdk module.
"""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import List

import typer

import iris.sdk as sdk

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   sdk CLI Module                                                     #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# create the typer object
main = typer.Typer()


@main.command()
def login():
    try:
        sdk.login()
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def logout():
    try:
        sdk.logout()
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def post(flags: List[str] = typer.Argument(None)):
    try:
        sdk.post(flags)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def get():
    try:
        sdk.get()
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def pull(experiment_cmd: str):
    try:
        sdk.pull(experiment_cmd)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@main.command()
def upload(
    src: str = typer.Argument(...),
    art_type: str = typer.Argument(...),
    name: str = typer.Argument(None),
    description: str = typer.Argument(None),
):
    try:
        sdk.upload(name, src, art_type, description)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
