from flask import jsonify, current_app as app, make_response, request
from statemachine.exceptions import TransitionNotAllowed, InvalidStateValue

from app import db
from app.models.hit import Hit
from app.models.hitman import Hitman
from app.models.managers_lackeys import ManagerLackey
from app.decorators.auth_decorator import validate_user
from app.state_machines.hitman_is_active_machine import HitmanIsActiveMachine


@app.route('/register', methods=['POST'])
def register():
    new_hitman = Hitman(name=request.json['name'],
                        email=request.json['email'],
                        level=request.json['level'])
    db.session.add(new_hitman)
    db.session.commit()

    return make_response(new_hitman.to_dict(), 201)


@app.route('/hitmen', methods=['GET'])
@validate_user
def get_hitmen(requester_id=None, requester_level=None):
    print(requester_id)
    print(requester_level)

    if requester_level == 'HITMAN':
        return make_response('insufficient privileges you are just a hitman :(', 403)
    elif requester_level == 'MANAGER':
        hitmen = Hitman.query.outerjoin(ManagerLackey, ManagerLackey.manager_id == requester_id) \
            .filter(Hitman.id == ManagerLackey.lackey_id).order_by(Hitman.created_at.asc()).all()
    else:
        hitmen = Hitman.query.order_by(Hitman.created_at.asc()).all()

    mapped_hitmen = [hitman.to_dict() for hitman in hitmen]

    return make_response(jsonify(mapped_hitmen), 200)


@app.route('/hitmen/<hitman_id>/status', methods=['PUT'])
@validate_user
def set_hitman_status(hitman_id, requester_id=None, requester_level=None):
    to_update_hitman = Hitman.query.filter(Hitman.id == hitman_id).first_or_404()
    request_status = request.json['is_active']
    status = HitmanIsActiveMachine(start_value=str(to_update_hitman.is_active).lower())

    try:
        if not request_status:
            status.deactivate()
        else:
            return make_response('can\'t reactivate hitmen', 400)
    except (TransitionNotAllowed, InvalidStateValue) as exception:
        return make_response(str(exception), 400)

    if requester_id == hitman_id:
        return make_response('can\'t deactivate yourself', 400)

    if requester_level == 'BOSS':
        deactivate_hitman(hitman_id)
        unassign_hits(hitman_id)

        response = make_response('ok', 200)
    elif requester_level == 'MANAGER':
        manager_lackey = ManagerLackey.query.filter(ManagerLackey.lackey_id == to_update_hitman.id).first()

        if manager_lackey and manager_lackey.manager_id == requester_id:
            deactivate_hitman(hitman_id)
            unassign_hits(hitman_id)

            response = make_response('ok', 200)
        else:
            response = make_response('you do not manage this guy :(', 403)
    else:
        response = make_response('insufficient privileges you are just a hitman :(', 403)

    return response


def deactivate_hitman(hitman_id):
    update_data = dict(is_active=False)

    Hitman.query.filter(Hitman.id == hitman_id).update(update_data)
    db.session.commit()


def unassign_hits(hitman_id):
    update_data = dict(hitman_id=None, assigned_by_id=None)

    Hit.query.filter(Hit.hitman_id == hitman_id).filter(Hit.is_active == True).update(update_data)
    db.session.commit()
