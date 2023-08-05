from functools import wraps

import typer

from release.exceptions import ReleaseException


def exit_nicely(f):
    """Catches expected exception and exit CLI nicely."""

    @wraps(f)
    def _wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ReleaseException as err:
            typer.secho(f"{err.msg}", err=True)
            raise typer.Exit(1)

    return _wrapper
