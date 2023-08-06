from typing import Any, Optional
import typer
from typer.core import TyperCommand
from typer.models import CommandFunctionType, Default

from lunni_cli.commands.create import create
from lunni_cli.commands.docker import dev, run
from lunni_cli.commands.version import version


app = typer.Typer()

app.command()(create)
app.command()(dev)
app.command(context_settings={"ignore_unknown_options": True})(run)
app.command()(version)
