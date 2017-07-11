import sys, re
import click
from itertools import groupby

from gramophone import gp

@click.group()
def cli():
    pass

@click.command()
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
@click.option('-m', '--model', default='model', help='prefix of the output model files')
@click.argument('data')
def train(mapping,model,data):
    """Train a model"""

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
    transcriber.save(model + ".crf")

    #
    # stage 3: language model training
    #
    click.echo(u"Stage 3: training rating n-gram language model", err=True)

    # the rater
    rater = gp.Rater()

    # train with previously aligned training data
    rater.train(aligned_training_data)

    # save
    rater.save(model + ".ngram")

    
@click.command()
@click.option('-M', '--mapping', required=True, help='grapheme-phoneme mapping')
@click.option('-c', '--crf', required=True, help='transcription CRF model')
@click.option('-l', '--language-model', 'lm', required=True, help='rating language model')
@click.argument('strings', nargs=-1)
def convert(mapping,crf,lm,strings):
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
        segmentations = aligner.scan(string)
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


cli.add_command(train)
cli.add_command(convert)
