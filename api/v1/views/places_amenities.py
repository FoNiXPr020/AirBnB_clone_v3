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
                 methods=["GET"])
def amenities_place(place_id):
    """show all amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    if request.method == "POST":
        if not request.is_json:
            abort(400, "Not a JSON")
        if "amenity_id" not in request.get_json():
            abort(400, "Missing amenity_id")
        if storage.get(Amenity, request.get_json()["amenity_id"]) is None:
            abort(404)


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["POST"])
def add_amenity_place(place_id):
    """add amenity to place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.is_json:
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
    else:
        abort(400, "Not a JSON")


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amenity_place(place_id, amenity_id):
    """delete amenity from place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200