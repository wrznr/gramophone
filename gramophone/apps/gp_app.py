from __future__ import absolute_import

from flask import Flask
from flask import request

def create_gp_app(aligner,transcriber,rater,formatter):
    app = Flask(__name__)

    @app.route('/gp/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':

            # get args
            strings = request.args.getlist('w')
            formats = request.args.getlist('f')

            oformat = ""
            if formats:
                oformat = formats[0]

            results = []
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
                results.append((string,u",".join(best_transcription),prob))

            return formatter.encode(results,oformat)

        elif request.method == 'POST':
            return str(request.form)

    return app
