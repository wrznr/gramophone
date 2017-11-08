from __future__ import absolute_import

import click

from gramophone import apps

@click.command()
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
def run(mapping):
    """
    Run the application
    """
    app = apps.create_gp_app(mapping)
    app.run()
