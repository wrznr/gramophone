from __future__ import absolute_import

import click

from gramophone import apps
from gramophone import gp

@click.command()
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
@click.option('-c', '--crf', required=True, help='transcription CRF model')
@click.option('-l', '--language-model', 'lm', required=True, help='rating language model')
def run(mapping,crf,lm):
    """
    Run the application
    """

    #
    # loading
    #
    click.echo(u"Loading...", err=True)

    click.echo(u"...data alignment", err=True)
    aligner = gp.Aligner(mapping=mapping)

    click.echo(u"...transcription CRF model", err=True)
    transcriber = gp.Transcriber()
    transcriber.load(crf)

    click.echo(u"...n-gram language model", err=True)
    rater = gp.Rater.load(lm)

    formatter = gp.Formatter()


    #
    # load app and run
    #
    app = apps.create_gp_app(aligner,transcriber,rater,formatter)
    app.run()

#000FB527B344
