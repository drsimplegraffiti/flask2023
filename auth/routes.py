from flask import request, jsonify, Blueprint, make_response
from flask_jwt_extended import create_access_token,  set_access_cookies, unset_jwt_cookies, jwt_required,get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import base64

from extensions import db
from models.users import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).one_or_none()

    if user is not None:
        return jsonify(message='username exist')

    hashed_password = generate_password_hash(password)

    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='user created')


@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).one_or_none()

    if user is not None and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': username, 'user_id': user.id})
        # Create a response with the access token
        response = jsonify(message='success', access_token=access_token)
        response.status_code = 200

        # Set the access token as a cookie in the response
        set_access_cookies(response, access_token)

        return response
    else:
        return jsonify(message='login failed'), 401

#update user profile_image as file


@auth.route('/profile_image', methods=['POST'])
@jwt_required()
def update_profile_image():
    try:
        profile_image = request.files['profile_image']
        decoded_user = get_jwt_identity()
        print(decoded_user)  # {'username': 'test', 'user_id': 1}

        if profile_image.filename != '':
            filename = secure_filename(profile_image.filename)
            profile_image.save(filename)
            with open(filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')  # Convert bytes to string
                user = User.query.get(decoded_user['user_id'])
                if user:
                    user.profile_image = encoded_string
                    db.session.commit()
                    return jsonify(message='Profile image updated')
                else:
                    return jsonify(message='User not found'), 404
        else:
            return jsonify(message='No profile image provided'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Profile image not updated'), 500
