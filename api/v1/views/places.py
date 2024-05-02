#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def cities(city_id):
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
def places(place_id):
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


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def cities_places_create(city_id):
    """create a new POST request """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    new_place = Place(city_id=city.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def places_update(place_id):
    """update a data request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    place.name = data.get("name", place.name)
    place.description = data.get("description",
                                 place.description)
    place.number_rooms = data.get("number_rooms",
                                  place.number_rooms)
    place.number_bathrooms = data.get("number_bathrooms",
                                      place.number_bathrooms)
    place.max_guest = data.get("max_guest", place.max_guest)
    place.price_by_night = data.get("price_by_night", place.price_by_night)
    place.latitude = data.get("latitude", place.latitude)
    place.longitude = data.get("longitude", place.longitude)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search():
    """
    Returns all Places that match the parameters in the
    JSON body of the request.
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    fromDB = request.get_json()

    if fromDB and len(fromDB):
        states = fromDB.get('states', None)
        cities = fromDB.get('cities', None)
        amenities = fromDB.get('amenities', None)

    if not fromDB or not len(fromDB) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        places_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)

    places_list = []
    if states:
        obj_states = [storage.get(State, s_id) for s_id in states]
        for state in obj_states:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places_list.append(place)

    if cities:
        obj_city = [storage.get(City, c_id) for c_id in cities]
        for city in obj_city:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        obj_amenities = [storage.get(Amenity, a_id) for a_id in amenities]
        places_list = [place for place in places_list
                       if all([am in place.amenities
                               for am in obj_amenities])]

    places = []
    for p in places_list:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
