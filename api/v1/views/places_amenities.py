#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
import os
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from flask import abort, request, jsonify

db_mode = os.getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET", "POST", "DELETE"])
def amenities_place(place_id):
    """retrieve place amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        if db_mode == "db":
            amenities = place.amenities
            amenities_list = [amenity.to_dict() for amenity in amenities]
        else:
            amenities_list = place.amenity_ids
        return jsonify(amenities_list)
    elif request.method == "POST":
        # Link a Amenity object to a Place:
        # POST /api/v1/places/<place_id>/amenities/<amenity_id>
        # No HTTP body needed
        # If the place_id is not linked to any Place object, raise a 404 error
        # If the amenity_id is not linked to any Amenity object, raise a 404 error
        # If the Amenity is already linked to the Place, return the Amenity with the status code 200
        # Returns the Amenity with the status code 201
        amenity_id = request.get_json()["amenity_id"]
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict(), 200)
        else:
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict(), 201)
    elif request.method == "DELETE":
        # Deleye an amenity my id
        # DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
        # If the place_id is not linked to any Place object, raise a 404 error
        # If the amenity_id is not linked to any Amenity object, raise a 404 error
        # If the Amenity is not linked to the Place before the request, raise a 404 error
        # Returns an empty dictionary with the status code 200
        amenity_id = request.get_json()["amenity_id"]
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}, 200)