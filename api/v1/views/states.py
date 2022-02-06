#!/usr/bin/python3
"""
Module: states
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def all_states():
    """Returning all states"""
    a_states = storage.all('State').values()  # storing all states values
    states = []  # empty list to store our values
    for i in a_states:  # parsing dictionary
        states.append(i.to_dict())
        # appending the values by state
    return jsonify(states)  # returning json with states info


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_list(state_id):
    """Retrieving a State by id"""
    objct = storage.get('State', state_id)  # storing our object
    if objct is None:  # verify it's present
        abort(404)  # otherwise throw 404 error
    objct = objct.to_dict()  # turn object into dictionary
    return jsonify(objct)  # return JSON form


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Method to delete a state by id"""
    objct = storage.get('State', state_id)  # Storing object from State class
    if objct is None:
        abort(404)
    storage.delete(objct)  # delete objct
    storage.save()  # update origin dict
    return make_response(jsonify({}), 200)
    # return empty dict with status code 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_states():
    """Post new information to States"""
    if not request.get_json:  # verify if there's a request.json
        abort(400, 'Not a JSON')  # otherwise return error 400
    state = request.json  # store given JSON
    if 'name' not in state.keys():  # verify name key availability
        abort(400, 'Missing name')
    new_state = State(**state)  # create a new instance with incoming data
    storage.new(new_state)  # create new state
    storage.save()  # save info in dict
    return make_response(jsonify(new_state.to_dict()), 201)
    # Return the new State with the status code 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def state_update(state_id):
    """Updating a State object by given id"""
    objct = storage.get('State', state_id)  # store State by given id
    if objct is None:  # check if it is valid
        abort(404)
    if not request.json:  # verify if there's a request.json
        abort(400, 'Not a JSON')  # otherwise return error 400
    state_update = request.json
    for key, value in state_update.items():
        # setting attributes Name & value to objct
        setattr(objct, key, value)
    storage.save()
    return make_response(jsonify(objct.to_dict()), 200)
