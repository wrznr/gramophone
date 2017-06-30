import click

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
    click.echo(u"Stage 1: training data alignment")

    # the aligner
    aligner = gp.Aligner(mapping=mapping)

    # iterate over input and align training data
    aligned_training_data = []
    with open(str(data),"r") as f:
        training_data = f.read()
        for line in training_data.split(u"\n"):

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

    click.echo(aligned_training_data)

    #
    # stage 2: crf training
    #

    # the transcriber
    transcriber = gp.Transcriber()
    transcriber.train(aligned_training_data,model + ".crfsuite")

    #
    # stage 3: language model training
    #

    
            

cli.add_command(train)
