#!/usr/bin/python3
"""
Module: Amenities
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """Returning all available amenities"""
    amenities = storage.all('Amenity').values()  # retrieving info from Amenity
    all_amenity = []
    for i in amenities:  # parsing info
        all_amenity.append(i.to_dict())  # storing in a new list as dict
    return jsonify(all_amenity)  # returning json with states info


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenities_list(amenity_id):
    """Retrieving an amenityity by id"""
    objct = storage.get('Amenity', amenity_id)  # storing our object
    if objct is None:  # verify it's present
        abort(404)  # otherwise throw 404 error
    objct = objct.to_dict()  # turn object into dictionary
    return jsonify(objct)  # return JSON form


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Method to delete an amenity by id"""
    objct = storage.get('Amenity', amenity_id)  # Storing object from Amenity
    if objct is None:
        abort(404)
    storage.delete(objct)  # delete objct
    storage.save()  # update origin dict
    return make_response(jsonify({}), 200)
    # return empty dict with status code 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenities():
    """Post new information to Amenity"""
    if not request.json:  # verify if there's a request.json
        abort(400, 'Not a JSON')  # otherwise return error 400
    objct = request.json  # store given JSON
    if 'name' not in objct.keys():  # verify name key availability
        abort(400, 'Missing name')
    new_amenity = Amenity(**objct)
    storage.new(new_amenity)  # create new amenity
    storage.save()  # save info in dict
    return make_response(jsonify(new_amenity.to_dict()), 201)
    # Return the new State with the status code 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """Updating an Amenity object by given id"""
    objct = storage.get('Amenity', amenity_id)  # store Amenity by given id
    if objct is None:  # check if it is valid
        abort(404)
    if not request.json:  # verify if there's a request.json
        abort(400, "Not a JSON")  # otherwise return error 400
    amenity_update = request.json
    for key, value in amenity_update.items():
        # setting attributes Name & value to objct
        setattr(objct, key, value)
    storage.save()
    return make_response(jsonify(objct.to_dict()), 200)
