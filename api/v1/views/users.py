#!/usr/bin/python3
"""
Module: users
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def all_users():
    """Returning all available users"""
    users = storage.all('User').values()  # retrieving info from User
    all_users = []
    for i in users:  # parsing info
        all_users.append(i.to_dict())  # storing in a new list as dict
    return jsonify(all_users)  # returning json with states info


@app_views.route('/users/<user_id>', strict_slashes=False)
def user_list(user_id):
    """Retrieving an User by given id"""
    objct = storage.get('User', user_id)  # storing our object
    if objct is None:  # verify it's present
        abort(404)  # otherwise throw 404 error
    objct = objct.to_dict()  # turn object into dictionary
    return jsonify(objct)  # return JSON form


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Method to delete an User by id"""
    objct = storage.get('User', user_id)  # Storing object from User
    if objct is None:
        abort(404)
    storage.delete(objct)  # delete object
    storage.save()  # update origin dict
    return make_response(jsonify({}), 200)
    # return empty dict with status code 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_users():
    """Post new information to User"""
    if not request.json:  # verify if there's a request.json
        abort(400, 'Not a JSON')  # otherwise return error 400
    objct = request.json  # store given JSON
    if 'email' not in objct.keys():  # verify email key availability
        abort(400, 'Missing email')
    if 'password' not in objct.keys():  # verify password key availability
        abort(400, 'Missing password')
    new_user = User(**objct)
    storage.new(new_user)  # create new user
    storage.save()  # save info in dict
    return make_response(jsonify(new_user.to_dict()), 201)
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
