"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from base64 import b64encode
import os
from api.utils import set_password, send_email
from datetime import timedelta
import cloudinary.uploader as uploader


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


expires_in_minutes = 10
expires_delta = timedelta(minutes=expires_in_minutes)



def check_password(hash_password, password, salt):
    return check_password_hash(hash_password, f"{password}{salt}")


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


#register user
@api.route("/user", methods=["POST"])
def add_user():
    data_form = request.form
    data_files = request.files

    data = {
        "lastname":data_form.get("lastname"),
        "email":data_form.get("email"),
        "password": data_form.get("password"),
        "avatar": data_files.get("avatar")
    }

    print(data)


    lastname = data.get("lastname", None)
    email = data.get("email", None)
    password = data.get("password", None)
    avatar = data.get("avatar", None)


    if email is None or password is None or lastname is None or avatar is None:
        return jsonify("you need an the email and a password"), 400
    
    else:
        # validar so el usuario exite
        user = User.query.filter_by(email=email).one_or_none()

        if user is not None : 
            return jsonify("user existe"), 400
        

        salt = b64encode(os.urandom(32)).decode("utf-8")
        password = set_password(password, salt)
        
        # guardo el avatar em la nube(cloudinary)
        result_cloud = uploader.upload(avatar)

        print(result_cloud.get("secure_url"))
        print(result_cloud.get("public_id"))


        # aqui es donde creamos el usuario a registrar
        user = User(
                email=email, password=password, 
                lastname=lastname, 
                salt=salt, 
                avatar=result_cloud.get("secure_url"), 
                public_id_avatar=result_cloud.get("public_id"))

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({"message":"User created"}), 201
            
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return jsonify({"message":f"error: {error}"}), 500

    # return jsonify("estamos trabajando por usted"), 201
        


@api.route("/user", methods=["GET"])
@jwt_required()
def get_all_users():
    user = User.query.get(get_jwt_identity())

    print(user)

    if user is None:
        return jsonify({"message":"user not found"}), 404

    return jsonify(user.serialize()), 200
    # else:
    #     return jsonify("NO autorizado, sorry"), 401



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
            if check_password(user.password, password, user.salt):
                token = create_access_token(identity=user.id)
                return jsonify({"token":token}), 200
            else:
                return jsonify({"message":"bad password"}), 400


#ruta que resetea el password
@api.route("/reset-password", methods=["POST"])
def reset_password():
    body = request.json

    # crear un link para poder recuperar la contraseña
    access_token = create_access_token(identity=body, expires_delta=expires_delta)

    # crear el mensaje a enviar por email

    message = f"""
        <h1> Si solicito recuperar la contraseña, ingrese al siguiente link</h1>
        <a href="{os.getenv("FRONTEND_URL")}password-update?token={access_token}">
            ir a recuperar contraseña
        </a>
    """

    data = {
        "subject": "Recuperación de contraseña",
        "to": body,
        "message": message
    }

    sended_email = send_email(data.get("subject"), data.get("to"), data.get("message"))

    print(sended_email)

    return jsonify("trabajando por un mejor servicio :)"), 200


# actualizamos el password
@api.route("/update-password", methods=["PUT"])
@jwt_required()
def update_pass():
    email = get_jwt_identity()
    body = request.json

    user = User.query.filter_by(email=email).one_or_none()

    if user is not None:
        salt = b64encode(os.urandom(32)).decode("utf-8")
        password = set_password(body, salt)

        user.salt = salt
        user.password= password

        try:
            db.session.commit()
            return jsonify("Clave actualizada bien"), 201
        except Exception as error:
            print(error.args)
            return jsonify("No se puede actualizar el password")


# enviar emails,
# guardar imagenes en cloudinary
# recuperar contraseña
