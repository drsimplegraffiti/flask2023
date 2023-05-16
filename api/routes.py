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

    # check if blog title already exists
    blog = Blog.query.filter_by(title=title).one_or_none()
    if blog is not None:
        return jsonify(message='Title already exists.'), 400

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

# get all blogs
@api.route('/blogs', methods=['GET'])
@jwt_required()
def get_all_blogs():
    try:
        blogs = Blog.query.all()
        blog_list = []
        for blog in blogs:
            blog_data = {
                'id': blog.id,
                'title': blog.title,
                'body': blog.body,
                'user_id': blog.user_id
            }
            blog_list.append(blog_data)
        return jsonify(blogs=blog_list), 200
    except Exception as e:
        print(e)
        return jsonify(message='Something went wrong.'), 500

# update blog that only belongs to you
@api.route('/blog/<int:blog_id>', methods=['PUT'])
@jwt_required()
def update_blog(blog_id):
    title = request.json.get("title")
    body = request.json.get("body")
    decoded_user = get_jwt_identity()
    print(decoded_user)

    # Check if the blog exists
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify(message='Blog not found.'), 404

    # Check if the blog belongs to the user
    if blog.user_id != decoded_user['user_id']:
        return jsonify(message='You are not authorized to update this blog.'), 403

    # Validate inputs
    if not title or not body:
        return jsonify(message='Title and body are required.'), 400
    if len(title) > 255:
        return jsonify(message='Title should not exceed 255 characters.'), 400
    if len(body) > 5000:
        return jsonify(message='Body should not exceed 5000 characters.'), 400

    # Check if the updated title already exists
    if title != blog.title:
        existing_blog = Blog.query.filter_by(title=title).first()
        if existing_blog:
            return jsonify(message='Title already exists.'), 400

    # Update the blog
    blog.title = title
    blog.body = body
    db.session.commit()

    return jsonify(message='Blog updated.'), 200

# delete blog that only belongs to you
@api.route('/blog/<int:blog_id>', methods=['DELETE'])
@jwt_required()
def delete_blog(blog_id):
    decoded_user = get_jwt_identity()
    print(decoded_user)

    # Check if the blog exists
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify(message='Blog not found.'), 404

    # Check if the blog belongs to the user
    if blog.user_id != decoded_user['user_id']:
        return jsonify(message='You are not authorized to delete this blog.'), 403

    db.session.delete(blog)
    db.session.commit()

    return jsonify(message='Blog deleted.'), 200