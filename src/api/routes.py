"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

def set_password(password):
    return generate_password_hash(password)


def check_password(hash_password, password):
    return check_password_hash(hash_password, password)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/user", methods=["POST"])
def add_user():
    body = request.json

    email = body.get("email", None)
    password = body.get("password", None)

    if email is None or password is None:
        return jsonify("you need an the email and a password"), 400
    
    else:
        password = set_password(password)
        user = User(email=email, password=password)



        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({"message":"User created"}), 201
            
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return jsonify({"message":f"error: {error}"}), 500
        


@api.route("/user", methods=["GET"])
@jwt_required()
def get_all_users():
    user = User.query.get(get_jwt_identity())

    if user.email == "deimianvasquez@gmail.com":
        user_all = User.query.all()
        user_all = list(map(lambda item: item.serialize(), user_all))
        return jsonify(user_all), 200
    else:
        return jsonify("NO aotorizado, sorry"), 401



@api.route("/login", methods=["POST"])
def login():
    body = request.json

    email = body.get("email", None)
    password = body.get("password", None)

    if email is None or password is None:
        return jsonify("you need an the email and a password"), 400

    # valido que el email enviado exista
    else:
        user = User()
        user = user.query.filter_by(email=email).one_or_none()  

        if user is None:
            return jsonify({"message":"bad email"}), 400
        else:
            if check_password(user.password, password):
                token = create_access_token(identity=user.id)
                return jsonify({"token":token}), 200
            else:
                return jsonify({"message":"bad password"}), 400

