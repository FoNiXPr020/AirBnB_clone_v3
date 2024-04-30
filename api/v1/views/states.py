#!/usr/bin/python3
"""new view for State objects that handles all 
default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify

@app_views.route("/states", methods=["GET"])
@app_views.route("/states/<string:state_id>", methods=["GET"])
def states(state_id=None):
    """retrieves an object into a valid Json"""
    states_id_list = []
    if state_id is None:
        all_objs = storage.all(State).values()
        for v in all_objs:
            states_id_list.append(v.to_dict())
        return jsonify(states_id_list)
    else:
        result = storage.get(State, state_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())
    
@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def states_delete(state_id=None):
    """Deletes a State object

    Args:
        state_id : a string that represent the id of the state
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=["Post"])
def create_state():
    """create a state object"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, message="Not a JSON")
    if "name" not in data:
        abort(400, message="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """update the state object
    Args:
        state_id : the state id
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, message="Not a JSON")
    state_obj["name"] = data["name"]
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200