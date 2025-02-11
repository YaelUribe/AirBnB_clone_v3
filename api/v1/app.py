#!/usr/bin/python3
"""Status of api"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
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
