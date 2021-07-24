from flask import request
from functools import wraps

from app.models.hitman import Hitman


def validate_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        requester_id = int(request.headers['user'])
        requester_level = Hitman.query.filter(Hitman.id == requester_id).first_or_404().level

        kwargs.update({'requester_id': requester_id, 'requester_level': requester_level})

        return f(*args, **kwargs)
    return decorated
