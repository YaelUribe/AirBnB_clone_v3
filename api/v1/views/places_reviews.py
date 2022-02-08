#!/usr/bin/python3
"""
Module: Review
"""
from api.v1.views import app_views
from models.review import Review
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False
)
def get_review_by_place(place_id):
    """Return review by place"""
    place = storage.get('Place', place_id)  # retrieving info from place
    if not place:  # Validating if exists
        abort(404)  # If not exists, error 404
    # Store object in dictionary
    reviews = [i.to_dict() for i in place.reviews]
    return jsonify(reviews)  # Return json with reviews info


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_review_by_id(review_id):
    """Retrieving a Review by id"""
    review = storage.get('Review', review_id)  # Retrieving info from review
    if not review:  # Verify it exists
        abort(404)  # If not exists error 404
    return jsonify(review)  # Return json with reviews info


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_review(review_id):
    """Delete a review by given id"""
    review = storage.get('Review', review_id)  # Retrieving info from review
    if not review:  # Verify it exists
        abort(404)  # If not exists error 404
    storage.delete(review)  # Delete info from review
    storage.save()  # Update Dictionary
    # Return a dictionary, 200 status code
    return make_response(jsonify({}), 200)


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
)
def create_review(place_id):
    """Create a Review by id"""

    if not request.json:  # verify if there's a request.json'
        abort(400, 'Not a JSON')  # If not is give a error 400 and stop process

    place = storage.get('Place', place_id)  # Retrieving info from Place

    if place is None:  # Verify if place exists
        abort(404)  # If not then abort and give 404 code

    user_id = request.json  # Assign and storage the json info gived

    if "user_id" not in user_id.keys():  # Compare if the given key exists
        abort(400, 'Missing user_id')  # Hola

    user = storage.get('User', user_id["user_id"])  # Verify if there is a

    if user is None:  # Verify if user exists
        abort(404)  # If not then abort and give 404 code

    if "text" not in user_id.keys():  # Compare if the given key exists
        abort(400, 'Missing text')  # If not then abort and give 400 code

    user_id["place_id"] = place_id

    new_review = Review(**user_id)

    storage.new(new_review)

    storage.save()

    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False,
    methods=['PUT']
)
def update_review(review_id):

    if not request.json:  # verify if there's a request.json'
        abort(400, 'Not a JSON')

    review_id = storage.get('Review', review_id)

    if review_id is None:
        abort(404)

    new_review = request.json

    for key, value in new_review.items():

        if key == 'id' or key == 'user_id' or key == 'place_id':
            continue

        setattr(review_id, key, value)

    storage.save()

    return make_response(jsonify(review_id.to_dict()), 200)
