#!/usr/bin/python3
"""sharing app_views Blueprint"""

from flask import Blueprint

from .index import *
from .states import *


app_views = Blueprint('app_views', __name__)
