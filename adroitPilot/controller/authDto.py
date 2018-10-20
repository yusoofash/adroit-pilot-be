import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from . import User
from bson.json_util import dumps
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

bp = Blueprint('auth', __name__)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_details = request.json['user']
        user = User()
        res = user.registerService(user_details)
        return jsonify(res)
    return jsonify('')


@bp.route("/users", methods=['GET'])
def users():
    user = User()
    all_users = user.getUsers()
    return jsonify(dumps(all_users))


@bp.route("/login", methods=['Get', 'POST'])
def login():
    if request.method == 'POST':
        user_details = request.json['user']
        email = user_details['email']
        password = user_details['password']
        if email is None:
            return jsonify({"msg": 'Email is required'}), 400
        elif password is None:
            return jsonify({"msg": 'Password is required'}), 400
        else:
            user = User()
            res = user.authenticate(email, password)
            return jsonify(res)
    return jsonify('')


@bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
