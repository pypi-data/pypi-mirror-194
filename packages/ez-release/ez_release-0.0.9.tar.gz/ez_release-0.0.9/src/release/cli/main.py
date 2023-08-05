import os

import typer
from git import Repo
from typer import Typer

from release.cli.bump import Parts, raise_on_non_main_branch, raise_on_dirty
from release.cli.helpers import exit_nicely
from release.git import get_latest_version, get_next_version

app = Typer(add_completion=False)


def show_version(flag: bool):
    if flag:
        from importlib.metadata import version

        typer.echo(f"release {version('release')}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=show_version, help="Show version."
    ),
):
    """Make release"""


@app.command()
@exit_nicely
def bump(
    part: Parts = "patch",
    push: bool = typer.Option(False, help="Whether to push tag to remote origin"),
    dry_run: bool = False,
    allow_non_main: bool = typer.Option(
        False, help="Whether to allow tagging a non main branch"
    ),
):
    """
    Bump version.
    """
    repo = Repo(os.getcwd(), search_parent_directories=True)

    if not allow_non_main:
        raise_on_non_main_branch(repo)

    raise_on_dirty(repo)

    current_version = get_latest_version(repo)
    next_version = get_next_version(repo, part=part.value)

    if dry_run:
        typer.echo("Dry run. None of the following will actually run.")
        typer.echo(f"Bumping {current_version} --> {next_version}")
    else:
        typer.echo(f"Bumping {current_version} --> {next_version}")
        repo.create_tag(f"{next_version}")
        if push:
            typer.echo(f"Pushing tag {next_version} to remote ...")
            repo.remotes.origin.push(f"{next_version}")
