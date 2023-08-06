import click
from konbini.cli.dataset import dataset


@click.group("cli")
@click.pass_context
def kon(ctx: str) -> None:
    """ The Konbini CLI, brought to you by folks at Hyperplane.
    """
    print(ctx)


kon.add_command(dataset)  # type: ignore

if __name__ == "__main__":
    kon()
