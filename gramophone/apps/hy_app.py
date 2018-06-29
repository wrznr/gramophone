from __future__ import absolute_import

from flask import Flask
from flask import request

def create_hy_app(coder,labeller,formatter):
    app = Flask(__name__)

    @app.route('/hy/', methods=['GET', 'POST'])
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
                encodement = coder.encode(string,mode="scan")
                labellings = labeller.label(encodement)
                combination = []
                for labelling in labellings:
                    for i in range(len(encodement)):
                        combination.append(u"%s\t%s" % (encodement[i],labelling[i]))
                    results.append((string,coder.decode(combination)))

            return formatter.encode(results, oformat)

        elif request.method == 'POST':
            return str(request.form)

    return app
