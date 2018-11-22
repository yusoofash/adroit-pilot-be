import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from ..services.auth import User
from ..services.company import Company
from bson.json_util import dumps
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

bp = Blueprint('auth', __name__)


@bp.route("/register/user", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        try:
            user_details = request.json['user']
        except:
            return jsonify('Invalid data given'), 400
        user = User()
        res = user.register_user(user_details)
        return dumps(res), 200
    return jsonify(''), 200


@bp.route("/register/company", methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        try:
            company_details = request.json['company']
        except:
            return jsonify('Invalid data given'), 400
        company = Company()
        res = company.register_company(company_details)
        return dumps(res), 200
    return jsonify(''), 200


@bp.route("/user/authenticate", methods=['Get', 'POST'])
def login_user():
    if request.method == 'POST':
        try:
            email = request.json['email']
            password = request.json['password']
        except Exception as err:
            return jsonify('Invalid data given', err), 400
        if email is None:
            return jsonify({"msg": 'Email is required'}), 400
        elif password is None:
            return jsonify({"msg": 'Password is required'}), 400
        else:
            user = User()
            res = user.authenticate_user(email, password)
            return dumps(res)
    return jsonify('')


@bp.route("/company/authenticate", methods=['Get', 'POST'])
def login_company():
    if request.method == 'POST':
        try:
            email = request.json['email']
            password = request.json['password']
        except:
            return jsonify('Invalid data given'), 400
        if email is None:
            return jsonify({"msg": 'Email is required'}), 400
        elif password is None:
            return jsonify({"msg": 'Password is required'}), 400
        else:
            company = Company()
            res = company.authenticate_company(email, password)
            return dumps(res)
    return jsonify('')


# @bp.route('/protected/user', methods=['GET'])
# @jwt_required
# def protected_user():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
#
#
# @bp.route('/protected/company', methods=['GET'])
# @jwt_required
# def protected_company():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
