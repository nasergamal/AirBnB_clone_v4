#!/usr/bin/python3
'''cities'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    ''' get all cities in state'''
    di = storage.get(State, state_id)
    if not di:
        abort(404)
    cities_list = []
    for city in di.cities:
        di = city.to_dict()
        cities_list.append(di)
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    '''get all cities or a specific state by id'''
    di = storage.get(City, city_id)
    if di:
        return jsonify(di.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    '''DELETE method'''
    di = storage.get(City, city_id)
    if not di:
        abort(404)
    storage.delete(di)
    storage.save()
    return jsonify({})


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    '''POST method'''
    di = storage.get(State, state_id)
    if not di:
        abort(404)
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in content:
        return make_response(jsonify({"error": "Missing name"}), 400)
    content['state_id'] = state_id
    ct = City(**content)
    storage.new(ct)
    storage.save()
    return (jsonify(ct.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    '''PUT method'''
    di = storage.get(City, city_id)
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
