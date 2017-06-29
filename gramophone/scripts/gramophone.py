import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--model', default=1, help='number of greetings')
@click.argument('data')
def train():
    """Train a model"""
    click.echo('Hello World!')

cli.add_command(train)
