#!/usr/bin/python3
'''users'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
@app_views.route('/users/<user_id>', strict_slashes=False)
def get_users(user_id=None):
    '''get all users or a specific user by id'''
    if not user_id:
        users_list = []
        for user in storage.all(User).values():
            di = user.to_dict()
            users_list.append(di)
        return jsonify(users_list)
    else:
        di = storage.get(User, user_id)
        if di:
            return jsonify(di.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    '''DELETE method'''
    di = storage.get(User, user_id)
    if not di:
        abort(404)
    storage.delete(di)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''POST method'''
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in content:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in content:
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**content)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    '''PUT method'''
    di = storage.get(User, user_id)
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
