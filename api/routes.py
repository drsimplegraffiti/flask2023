from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required,get_jwt_identity
from random import randint
from models.users import User
from models.blog import Blog
from extensions import db

api = Blueprint('api', __name__)

@api.route('/random', methods=['GET'])
@jwt_required()
def generate_random_number():
    # print the current identity (id of the current user)
    username = get_jwt_identity()
    print(username)
    return jsonify({
        'message': 'Success for username: {}'.format(username),
        'random_number': randint(1, 100)}), 200


#create blog post by user
@api.route('/blog', methods=['POST'])
@jwt_required()
def create_blog():
    title = request.json.get("title")
    body = request.json.get("body")
    decoded_user = get_jwt_identity()
    print(decoded_user)  # {'username': 'test', 'user_id': 1}

    # Validate inputs
    if not title or not body:
        return jsonify(message='Title and body are required.'), 400
    if len(title) > 255:
        return jsonify(message='Title should not exceed 255 characters.'), 400
    if len(body) > 5000:
        return jsonify(message='Body should not exceed 5000 characters.'), 400

    user = User.query.filter_by(id=decoded_user['user_id']).one_or_none()
    if user is None:
        return jsonify(message='User not found.')

    blog = Blog(title=title, body=body, user_id=user.id)
    db.session.add(blog)
    db.session.commit()
    return jsonify(message='Blog created.')
