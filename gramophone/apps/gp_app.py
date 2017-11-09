from __future__ import absolute_import

from flask import Flask
from flask import request

def create_gp_app(aligner,transcriber,rater):
    app = Flask(__name__)

    @app.route('/gp/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':

            results = []
            strings = request.args.getlist('w')
            for string in strings:
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
                results.append(u",".join(best_transcription))

            return str(results)

        elif request.method == 'POST':
            return str(request.form)

    return app
