#!/usr/bin/python3
"""Status of api"""
from logging import error
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """Close Storage"""
    storage.close()


@app.errorhandler(404)  # Errors handle by code or exception class
def nope(error):
    """Handling error 404"""
    nope = {"error": "Not found"}
    return make_response(jsonify(nope), 404)
    # This creates a response with a 404 error code
    # by setting an additional header view


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True)
