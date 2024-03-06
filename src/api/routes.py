"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Favorite
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/user', methods=['GET', "POST"])
def handle_user():
    if request.method == 'GET':
        users = User.query.all()
        users = list(map(lambda user: user.to_dict(), users))

        return jsonify({
            "data": users
        }), 200
    elif request.method == 'POST':
        user = User()
        data = request.get_json()
        user.name = data["name"]
        user.username = data["username"]
        user.password = data["password"]

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "msg": "user created"
        }), 200

@api.route("/user/<int:id>", methods=["GET","PUT", "DELETE"])
def update_user(id):
    if request.method == 'GET':
        user_id = id
        user = User.query.get(id)
        data = user.to_dict()

        return data, 200
    elif request.method == 'PUT':
        user = User.query.get(id)
        if user is not None:
            data = request.get_json()
            user.name = data["name"]
            user.username = data["username"]
            db.session.commit()
            return jsonify({
                "msg":"user updated"
            }),200
        else:
            return jsonify({
                "msg": "user not found"
            }), 404
    elif request.method == 'DELETE':
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()

            return jsonify({
                "msg":"user deleted"
            }),202
        else:
            return jsonify({
                "msg":"user not found"
            }), 404

@api.route('/character', methods=['GET', "POST"])
def handle_character():
    if request.method == 'GET':
        characters = Character.query.all()
        characters = list(map(lambda character: character.to_dict(), characters))

        return jsonify({
            "data": characters
        }), 200
    elif request.method == 'POST':
        character = Character()
        data = request.get_json()
        character.name = data["name"]

        db.session.add(character)
        db.session.commit()

        return jsonify({
            "msg": "character created"
        }), 200

@api.route("/character/<int:id>", methods=["PUT", "DELETE"])
def update_character(id):
    if request.method == 'PUT':
        character = Character.query.get(id)
        if character is not None:
            data = request.get_json()
            character.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"character updated"
            }),200
        else:
            return jsonify({
                "msg": "character not found"
            }), 404
    elif request.method == 'DELETE':
        character = Character.query.get(id)
        if character is not None:
            db.session.delete(character)
            db.session.commit()

            return jsonify({
                "msg":"character deleted"
            }),202
        else:
            return jsonify({
                "msg":"character not found"
            }), 404

@api.route('/planet', methods=['GET', "POST"])
def handle_planet():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.to_dict(), planets))

        return jsonify({
            "data": planets
        }), 200
    elif request.method == 'POST':
        planet = Planet()
        data = request.get_json()
        planet.name = data["name"]

        db.session.add(planet)
        db.session.commit()

        return jsonify({
            "msg": "planet created"
        }), 200

@api.route("/planet/<int:id>", methods=["PUT", "DELETE"])
def update_planet(id):
    if request.method == 'PUT':
        planet = Planet.query.get(id)
        if planet is not None:
            data = request.get_json()
            planet.name = data["name"]
            db.session.commit()
            return jsonify({
                "msg":"planet updated"
            }),200
        else:
            return jsonify({
                "msg": "planet not found"
            }), 404
    elif request.method == 'DELETE':
        planet = Planet.query.get(id)
        if planet is not None:
            db.session.delete(planet)
            db.session.commit()

            return jsonify({
                "msg":"planet deleted"
            }),202
        else:
            return jsonify({
                "msg":"planet not found"
            }), 404

@api.route('/user/<int:id>/favorite', methods=['GET'])
def handle_favorite(id):
    user_id = id
    favorites = Favorite.query.filter_by(user_id=user_id)
    favorites = list(map(lambda favorite: favorite.to_dict(), favorites))

    return jsonify({
        "data": favorites
    }), 200
    
@api.route('/favorite', methods=["POST"])
def create_favorite():
    favorite = Favorite()
    data = request.get_json()
    user_id = data["user_id"]
    if data["character_id"] is None:
        character_id = "0"
    character_id = data["character_id"]
    if data["planet_id"] is None:
        planet_id = "0"
    planet_id = data["planet_id"]
    

    user_filter = User.query.filter_by(id=user_id)
    character_filter = Character.query.filter_by(id=character_id)
    planet_filter = Planet.query.filter_by(id=planet_id)

    if user_filter is not None and character_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_character = data["character_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "favorite created"
        }), 200

    elif user_filter is not None and planet_filter is not None:
        favorite.user_id = data["user_id"]
        favorite.user_planet = data["planet_id"]
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
        "msg": "favorite created"
        }), 200

    else:
        return jsonify({
                "msg":"favorite could not be create, make sure user, character or planet exists"
            }), 404
