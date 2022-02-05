#!/usr/bin/python3
"""
module: index
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON file with status: ok"""
    return jsonify({"status": "OK"})
