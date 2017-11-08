from __future__ import absolute_import

from flask import Flask

def create_gp_app(mapping):
    app = Flask(__name__)

    @app.route('/gp')
    def index():
        return mapping

    return app
