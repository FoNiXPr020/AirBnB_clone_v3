#!/usr/bin/python3xx
'''api status'''
import models
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    '''return stuff'''
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route('/stats', strict_slashes=False)
def stuff():
    '''JSON Responses'''
    types = {'states': State, 'users': User,
            'amenities': Amenity, 'cities': City,
            'places': Place, 'reviews': Review}
    for key in types:
        types[key] = storage.count(types[key])
    return jsonify(types)
