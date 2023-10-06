#!/usr/bin/python3
'''places reviews'''
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    ''' get all reviews in a place'''
    di = storage.get(Place, place_id)
    if not di:
        abort(404)
    reviews_list = []
    for review in di.reviews:
        di = review.to_dict()
        reviews_list.append(di)
    return jsonify(reviews_list)


@app_views.route('reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    '''get all places or a specific place by id'''
    di = storage.get(Review, review_id)
    if di:
        return jsonify(di.to_dict())
    abort(404)


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    '''DELETE method'''
    di = storage.get(Review, review_id)
    if not di:
        abort(404)
    storage.delete(di)
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    '''POST method'''
    di = storage.get(Place, place_id)
    if not di:
        abort(404)
    content = request.get_json()
    if not content:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in content:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if not storage.get(User, content['user_id']):
        abort(404)
    if "text" not in content:
        return make_response(jsonify({"error": "Missing text"}), 400)
    content['place_id'] = place_id
    ct = Review(**content)
    storage.new(ct)
    storage.save()
    return (jsonify(ct.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    '''PUT method'''
    di = storage.get(Review, review_id)
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
