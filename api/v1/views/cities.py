#!/usr/bin/python3
"""
Module: Cities
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """Returning all cities of a state"""
    state = storage.get('State', state_id)  # retrieving info of state
    if state is None:  # verify presence of State by given id
        abort(404)
    for i in state.cities:  # parsing State
        cities = [i.to_dict()]  # storing in a new list
    return jsonify(cities)  # returning json with states info


@app_views.route('/cities/<city_id>', strict_slashes=False)
def cities_list(city_id):
    """Retrieving a city by id"""
    objct = storage.get('City', city_id)  # storing our object
    if objct is None:  # verify it's present
        abort(404)  # otherwise throw 404 error
    objct = objct.to_dict()  # turn object into dictionary
    return jsonify(objct)  # return JSON form


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Method to delete a city by id"""
    objct = storage.get('City', city_id)  # Storing object from State class
    if objct is None:
        abort(404)
    storage.delete(objct)  # delete objct
    storage.save()  # update origin dict
    return make_response(jsonify({}), 200)
    # return empty dict with status code 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id):
    """Post new information to city in a given State"""
    if not request.json:  # verify if there's a request.json
        abort(400, 'Not a JSON')  # otherwise return error 400
    objct = request.json  # store given JSON
    if 'name' not in objct.keys():  # verify name key availability
        abort(400, 'Missing name')
    state = storage.get('State', state_id)  # Getting State info
    if state is None:
        abort(404)
    objct['state_id'] = state_id  # assign state Id to new city
    new_city = City(**objct)
    storage.new(new_city)  # create new state
    storage.save()  # save info in dict
    return make_response(jsonify(new_city.to_dict()), 201)
    # Return the new State with the status code 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_update(city_id):
    """Updating a State object by given id"""
    objct = storage.get('City', city_id)  # store State by given id
    if objct is None:  # check if it is valid
        abort(404)
    if not request.json:  # verify if there's a request.json
        abort(400, "Not a JSON")  # otherwise return error 400
    city_update = request.json
    for key, value in city_update.items():
        # setting attributes Name & value to objct
        setattr(objct, key, value)
    storage.save()
    return make_response(jsonify(objct.to_dict()), 200)
