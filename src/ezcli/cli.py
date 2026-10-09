"""Command-line entry point for EZcli."""

import typer

from ezcli.tui import run

app = typer.Typer(
    name="ezcli",
    help="A local assistant for generating Bash commands.",
)


@app.callback(invoke_without_command=True)
def main() -> None:
    """Launch the interactive terminal interface."""
    run()


if __name__ == "__main__":
    app()