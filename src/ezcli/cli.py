"""Command-line entry point for EZcli."""

import typer

app = typer.Typer(
    name="ezcli",
    help="A command-line tool for working with text.",
)


@app.command()
def main() -> None:
    """Display a welcome message."""
    typer.echo("Welcome to EZcli!")


if __name__ == "__main__":
    app()
