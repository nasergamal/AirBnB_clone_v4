#!/usr/bin/python3
'''states'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id=None):
    '''get all states or a specific state by id'''
    if not state_id:
        states_list = []
        for state in storage.all(State).values():
            di = state.to_dict()
            states_list.append(di)
        return jsonify(states_list)
    else:
        di = storage.get(State, state_id)
        if di:
            return jsonify(di.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    '''DELETE method'''
    di = storage.get(State, state_id)
    if not di:
        abort(404)
    storage.delete(di)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    '''POST method'''
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in content:
        return make_response(jsonify({"error": "Missing name"}), 400)
    st = State(**content)
    storage.new(st)
    storage.save()
    return (jsonify(st.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    '''PUT method'''
    di = storage.get(State, state_id)
    if not di:
        abort(404)
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in content.items():
        if k not in ['id', 'created_at', 'updated']:
            setattr(di, k, v)
    storage.save()
    return jsonify(di.to_dict())
