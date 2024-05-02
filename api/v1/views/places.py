#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def places(city_id):
    """show places"""
    places_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def places_get(place_id):
    """Retrieves a City object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def places_delete(place_id):
    """delete a data request"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200




@app_views.route("/places_search", strict_slashes=False, methods=["POST"])
def places_search():
    """retrieve Place objects from a JSON body"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])
    if not states and not cities:
        places = storage.all(Place)
    else:
        places = []
        for city in storage.all(City):
            if city.state_id in states or city.id in cities:
                places.extend(city.places)
        places = list(set(places))
    if amenities:
        places_with_amenities = []
        for place in places:
            for amenity in place.amenities:
                if amenity.id in amenities:
                    places_with_amenities.append(place)
                    break
        places = places_with_amenities
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)

    return jsonify(place.to_dict()), 200
