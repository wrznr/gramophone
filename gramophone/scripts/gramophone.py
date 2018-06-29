# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys, re
import click
from itertools import groupby

from gramophone import gp
from gramophone import hy

@click.group()
def cli():
    pass

@click.group()
def GP(name="gp"):
    """Grapheme-phoneme conversion"""
    pass

@click.group()
def HY(name="hy"):
    """Hyphenation"""
    pass

@GP.command(name="train")
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
@click.option('-m', '--model', default='model', help='prefix of the output model files')
@click.argument('data')
def train_gp(mapping,model,data):
    """Train a model."""

    #
    # stage 1: alignment
    #
    click.echo(u"Stage 1a: creating data alignment", err=True)

    # the aligner
    aligner = gp.Aligner(mapping=mapping)

    click.echo(u"Stage 1b: aligning training data", err=True)
    # iterate over input and align training data
    aligned_training_data = []
    with open(str(data),"r") as f:
        training_data = f.read()

        with click.progressbar(training_data.split(u"\n")) as bar:
            for line in bar:

                # skip comments
                if line.startswith(u"#"):
                    continue

                # assume tab-separated values
                fields = line.split(u"\t")
                if len(fields) < 2:
                    continue

                # align
                alignment = aligner.align(fields[0],fields[1])
                aligned_training_data.append(alignment)

    #
    # stage 2: crf training
    #
    click.echo(u"Stage 2: training transcription CRF model", err=True)

    # the transcriber
    transcriber = gp.Transcriber()

    # train with previously aligned training data
    transcriber.train(aligned_training_data)

    # save
    transcriber.save(model + ".gp.crf")

    #
    # stage 3: language model training
    #
    click.echo(u"Stage 3: training rating n-gram language model", err=True)

    # the rater
    rater = gp.Rater()

    # train with previously aligned training data
    rater.train(aligned_training_data)

    # save
    rater.save(model + ".gp.ngram")

    
@GP.command(name="apply")
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
@click.option('-c', '--crf', required=True, help='transcription CRF model')
@click.option('-l', '--language-model', 'lm', required=True, help='rating language model')
@click.argument('strings', nargs=-1)
def apply_gp(mapping,crf,lm,strings):
    """Convert strings"""

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


    #
    # conversion
    #

    # read input
    in_strings = []
    if strings and strings[0] == u"-":
        for line in sys.stdin:
            in_strings.append(line.strip())
    elif strings:
        for datum in strings:
            in_strings.append(datum)
    else:
        pass

    # convert
    for string in in_strings:
        segmentations = aligner.scan(string.lower())
        best_transcription = []
        best_prob = 0.0
        for segmentation in segmentations:
            transcriptions = transcriber.transcribe(segmentation)
            for transcription in transcriptions:
                prob = rater.rate([segmentation,transcription])
                #click.echo("%s: %f" % (u",".join(transcription),prob), err=True)
                if prob >= best_prob:
                    best_prob = prob
                    best_transcription = transcription
        click.echo(u",".join(best_transcription))


GP.add_command(train_gp)
GP.add_command(apply_gp)
cli.add_command(GP)

@HY.command(name="train")
@click.option('-m', '--model', default='model', help='prefix of the output model files')
@click.argument('data')
def train_hy(model,data):
    """Train a model"""

    #
    # stage 1: read
    #
    click.echo(u"Stage 1: Encoding training data", err=True)
    coder = hy.Coder()

    # iterate over input
    encoded_training_data = []
    with open(str(data),"r") as f:
        training_data = f.read()

        with click.progressbar(training_data.split(u"\n")) as bar:
            for line in bar:

                # skip comments
                if line.startswith(u"#"):
                    continue

                # assume tab-separated values
                fields = line.split(u"\t")
                if len(fields) < 2:
                    continue

                # encode
                encodement = coder.encode(fields[1])
                encoded_training_data.append(encodement)

    #
    # stage 2: crf training
    #
    click.echo(u"Stage 2: training labelling CRF model", err=True)

    # the transcriber
    labeller = hy.Labeller()

    # train with previously read training data
    labeller.train(encoded_training_data)

    # save
    labeller.save(model + ".hy.crf")
    
@HY.command(name="apply")
@click.option('-c', '--crf', required=True, help='hyphenation CRF model')
@click.argument('strings', nargs=-1)
def apply_hy(crf,strings):
    """Convert strings"""

    #
    # loading
    #
    click.echo(u"Loading...", err=True)

    click.echo(u"...coder", err=True)
    coder = hy.Coder()

    click.echo(u"...hyphenation CRF model", err=True)
    labeller = hy.Labeller()
    labeller.load(crf)

    #
    # conversion
    #

    # read input
    in_strings = []
    if strings and strings[0] == u"-":
        for line in sys.stdin:
            in_strings.append(line.strip())
    elif strings:
        for datum in strings:
            in_strings.append(datum)
    else:
        pass

    # convert
    for string in in_strings:
        encodement = coder.encode(string,mode="scan")
        labellings = labeller.label(encodement)
        combination = []
        for labelling in labellings:
            for i in range(len(encodement)):
                combination.append(u"%s\t%s" % (encodement[i],labelling[i]))
            click.echo(coder.decode(combination))

@HY.command(name="import")
@click.option('-f', '--format', default='dwds', help='Input file format', type=click.Choice(['dwds']))
@click.argument('data')
def import_hy(format,data):
    """Import data for training"""

    with open(str(data),"r") as f:
        conversion_data = f.read()

        out_data = {}
        with click.progressbar(conversion_data.split(u"\n")) as bar:
            for line in bar:
                fields = line.split(u',')
                if len(fields) != 3:
                    continue
                in_words = fields[2].split(u' | ')
                out_syl = fields[1].split(u' · ')
                # TODO: Discuss with @haoess
                if len(in_words) != len(out_syl):
                    continue
                for i in range(0,len(in_words)):
                    click.echo(u"%s\t%s" % (in_words[i].strip(u'"').replace(u'·', u'-'), re.sub(u"(?<!^)-",u"·",out_syl[i].strip(u'"'))))


HY.add_command(train_hy)
HY.add_command(apply_hy)
HY.add_command(import_hy)
cli.add_command(HY)
