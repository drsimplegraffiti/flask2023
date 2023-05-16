from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from random import randint
from extensions import jwt

api = Blueprint('api', __name__)

@api.route('/random', methods=['GET'])
@jwt_required()
def generate_random_number():
    return jsonify({
        'message': 'Success',
        'random_number': randint(1, 100)}), 200