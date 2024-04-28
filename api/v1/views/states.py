#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST", "DELETE"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET", "PUT", "DELETE"])
def states(state_id=None):
    """show states and states with id"""
    states_list = []
    if state_id is None:
        all_objs = storage.all(State).values()
        for v in all_objs:
            states_list.append(v.to_dict())
        return jsonify(states_list)

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj.to_dict())

    if request.method == "DELETE":
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        data = request.get_json(force=True, silent=True)
        if not data:
            abort(400, "Not a JSON")
        obj.name = data.get("name", obj.name)
        obj.save()
        return jsonify(obj.to_dict()), 200

    if request.method == "POST":
        data = request.get_json(force=True, silent=True)
        if not data:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

