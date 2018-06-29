from __future__ import absolute_import

import click

from gramophone import apps
from gramophone import gp
from gramophone import hy

@click.group()
def cli():
    pass

@cli.command(name="gp")
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
@click.option('-c', '--crf', required=True, help='transcription CRF model')
@click.option('-l', '--language-model', 'lm', required=True, help='rating language model')
def run_gp(mapping,crf,lm):
    """
    Run the g2p server.
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

    click.echo(u"...output formatter", err=True)
    formatter = gp.Formatter()


    #
    # load app and run
    #
    app = apps.create_gp_app(aligner,transcriber,rater,formatter)
    app.run()

@cli.command(name="hy")
@click.option('-c', '--crf', required=True, help='hyphenation CRF model')
def run_hy(crf):
    """
    Run the hyphenation server.
    """

    #
    # loading
    #
    click.echo(u"Loading...", err=True)

    click.echo(u"...coder", err=True)
    coder = hy.Coder()

    click.echo(u"...hyphenation CRF model", err=True)
    labeller = hy.Labeller()
    labeller.load(crf)

    click.echo(u"...output formatter", err=True)
    formatter = hy.Formatter()

    #
    # load app and run
    #
    app = apps.create_hy_app(coder, labeller, formatter)
    app.run()
