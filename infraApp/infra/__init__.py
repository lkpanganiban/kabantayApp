from flask import Blueprint
infra = Blueprint('infra', __name__)
from . import routes
