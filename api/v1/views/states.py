#!/usr/bin/python3
''' new view for State objects'''
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import name
from models.state import State
import models
from models import storage


@app_views.route("/states", method=['GET'], strict_slashes=False)
def get_method():
    """retrieve all the data related to state object"""
    objects = storage.all("State")
    list_states = []
    for state in objects.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)

