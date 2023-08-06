import click


@click.group("dataset", invoke_without_command=True)
@click.pass_context
def dataset(ctx: str) -> None:
    """Konbini data stores"""
    print(ctx)
