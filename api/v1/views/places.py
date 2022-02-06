#!/usr/bin/python3
"""
Module: places
"""
from AirBnB_clone_v3.api.v1.views import cities
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Returning all available places"""
    city = storage.get('City', city_id)  # retrieving info from User
    if city is None:  # validating id presence
        abort(404)
    places = [i.to_dict() for i in city.places]
    return jsonify(places)  # returning json with places info


@app_views.route('/places/<place_id>>', strict_slashes=False)
def places_list(place_id):
    """Retrieving a Place by given id"""
    objct = storage.get('Place', place_id)  # storing our object
    if objct is None:  # verify it's present
        abort(404)  # otherwise throw 404 error
    objct = objct.to_dict()  # turn object into dictionary
    return jsonify(objct)  # return JSON form


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Method to delete a Place by id"""
    objct = storage.get('Place', place_id)  # Storing object from User
    if objct is None:
        abort(404)
    storage.delete(objct)  # delete object
    storage.save()  # update origin dict
    return make_response(jsonify({}), 200)
    # return empty dict with status code 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """Post new information to Place"""
    if not request.json:  # verify if there's a request.json
        abort(400, 'Not a JSON')  # otherwise return error 400

    city = storage.get('City', city_id)  # retrieve city by id
    if city is None:  # validate availability
        abort(404)

    objct = request.json  # store given JSON
    if 'user_id' not in objct.keys():  # verify email key availability
        abort(400, 'Missing user_id')

    user = storage.get('User', objct['user_id'])
    if user is None:
        abort(400)

    if 'name' not in objct.keys():
        abort(400, "Missing name")

    objct['city_id'] = city_id
    new_place = Place(**objct)
    storage.new(new_place)  # create new user
    storage.save()  # save info in dict
    return make_response(jsonify(new_place.to_dict()), 201)
    # Return the new State with the status code 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def users_update(user_id):
    """Updating an Amenity object by given id"""
    objct = storage.get('User', user_id)  # store Amenity by given id
    if objct is None:  # check if it is valid
        abort(404)
    if not request.json:  # verify if there's a request.json
        abort(400, "Not a JSON")  # otherwise return error 400
    user_update = request.json
    for key, value in user_update.items():
        # setting attributes Name & value to objct
        setattr(objct, key, value)
    storage.save()
    return make_response(jsonify(objct.to_dict()), 200)