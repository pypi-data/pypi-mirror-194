"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """GPT Context."""


if __name__ == "__main__":
    main(prog_name="gpt-context")  # pragma: no cover
