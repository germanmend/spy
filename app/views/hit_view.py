from flask import request, current_app as app, make_response, jsonify
from statemachine.exceptions import TransitionNotAllowed, InvalidStateValue

from app import db
from app.models.hit import Hit
from app.models.hitman import Hitman
from app.models.managers_lackeys import ManagerLackey
from app.state_machines.hit_status_machine import HitStatusMachine
from app.decorators.auth_decorator import validate_user


@app.route('/hits/create', methods=['POST'])
@validate_user
def create(requester_level=None):
    if requester_level == 'HITMAN':
        return make_response('insufficient privileges you are just a hitman :(', 403)

    new_hit = Hit(description=request.json['description'],
                  target=request.json['target']
                  )
    db.session.add(new_hit)
    db.session.commit()

    return make_response(new_hit.to_dict(), 201)


@app.route('/hits', methods=['GET'])
@validate_user
def get_hits(requester_id=None, requester_level=None):
    if requester_level == 'HITMAN':
        hits = Hit.query.filter(Hit.hitman_id == requester_id).order_by(Hit.created_at.asc())
    elif requester_level == 'MANAGER':
        hits = Hit.query.outerjoin(ManagerLackey, ManagerLackey.manager_id == requester_id) \
            .filter((Hit.hitman_id == requester_id) | (Hit.hitman_id == ManagerLackey.lackey_id))
    else:
        hits = Hit.query.order_by(Hit.created_at.asc()).all()

    mapped_hits = [hit.to_dict() for hit in hits]

    return make_response(jsonify(mapped_hits), 200)


@app.route('/hits/<hit_id>', methods=['GET'])
@validate_user
def get_by_id(hit_id, requester_id=None, requester_level=None):
    hit = Hit.query.filter(Hit.id == hit_id).first_or_404()

    if hit.hitman_id == requester_id or requester_level == 'BOSS':
        return make_response(hit.to_dict(), 200)
    elif requester_level == 'MANAGER':
        manager_lackey = ManagerLackey.query.filter(ManagerLackey.lackey_id == hit.hitman_id).first()

        response = make_response(hit.to_dict(), 200) if manager_lackey and manager_lackey.manager_id == requester_id\
            else make_response('can\'t see this hit insufficient permissions :(', 403)

        return response

    else:
        return make_response('can\'t see this hit insufficient permissions :(', 403)


@app.route('/hits/<hit_id>/status', methods=['PUT'])
@validate_user
def set_hit_status(hit_id, requester_id=None, requester_level=None):
    hit = Hit.query.filter(Hit.id == hit_id).first_or_404()
    status = HitStatusMachine(start_value=hit.status)
    request_status = request.json['status']

    try:
        if request_status == 'completed':
            status.toCompleted()
        if request_status == 'failed':
            status.toFailed()
    except (TransitionNotAllowed, InvalidStateValue) as exception:
        return make_response(str(exception), 400)

    if hit.hitman_id == requester_id or requester_level == 'BOSS':
        update_hit_status(hit.id, request_status)

        return make_response('OK', 200)

    else:
        manager_lackey = ManagerLackey.query.filter(ManagerLackey.lackey_id == hit.hitman_id).first()

        if manager_lackey and manager_lackey.manager_id == requester_id:
            updateHitStatus(hit.id, request_status)

            return make_response('OK', 200)

        else:
            return make_response('insufficient permissions you are not the hitman\'s manager :(', 403)


@app.route('/hits/<hit_id>/assign', methods=['PUT'])
@validate_user
def assign(hit_id, requester_id=None, requester_level=None):
    if requester_level == 'HITMAN':
        return make_response('insufficient you are just a hitman :(', 403)

    hit = Hit.query.filter(Hit.id == hit_id).first_or_404()
    hitman_to_assign = Hitman.query.filter(Hitman.id == int(request.json['hitman_id'])).first_or_404()

    if hitman_to_assign == requester_id or hit.is_active or hit.hitman or not hitman_to_assign.is_active:
        return make_response('invalid hit or hitman to assign assigned :(', 400)

    if requester_level in ('MANAGER', 'BOSS'):
        manager_lackey = ManagerLackey.query.filter(ManagerLackey.lackey_id == hitman_to_assign.id).first()

        if (manager_lackey and manager_lackey.manager_id == requester_id) or requester_level == 'BOSS':
            update_data = dict(is_active=True, hitman_id=hitman_to_assign.id, assigned_by_id=requester_id)

            Hit.query.filter(Hit.id == hit_id).update(update_data)
            db.session.commit()

            return make_response('OK', 200)
        else:
            return make_response('insufficient permissions you are not the hitman\'s manager :(', 403)


def update_hit_status(hit_id, status):
    update_data = dict(status=status, is_active=False)

    Hit.query.filter(Hit.id == hit_id).update(update_data)
    db.session.commit()
