#!/usr/bin/python3
"""
Module: Review
"""
from api.v1.views import app_views
from models.review import Review
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route(
    '/api/v1/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False
)
def get_review_by_place(place_id):
    """"""

    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = place.reviews()
    # TODO: Create a empty list for enter all reviews but, each one at the time. Crear lista vacía y luego for review en reviews. Y a cada review
    # se le hace .to_dict. For review in reviews.my_list.append(review.to_dict())
    return jsonify(reviews)


@app_views.route(
    '/api/v1/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_review_by_id(review_id):
    """"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    return jsonify(review)


@app_views.route(
    '/api/v1/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_review(review_id):
    """"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return make_response(jsonify({}), 200)


@app_views.route(
    '/api/v1/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
)
def create_review(place_id):
    """"""
    if not storage.get('Place', place_id):
        abort(404)
    review_json = request.get_json()

    if not review_json:
        abort(400, 'Not a JSON')
    review = Review(**review_json)

    if 'user_id' not in review_json.keys():
        abort(400, 'Missing user_id')

    user = storage.get('User', review.user_id)
    
    if 'user_id' not in user:
        abort(400)
