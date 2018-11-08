import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from ..services.auth import (
    User, Company
)

from bson.json_util import dumps
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
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
        res = user.registerUser(user_details)
        return jsonify(res)
    return jsonify('')


@bp.route("/register/company", methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        try:
            company_details = request.json['company']
        except:
            return jsonify('Invalid data given'), 400
        company = Company()
        res = company.registerCompany(company_details)
        return jsonify(res)
    return jsonify('')


@bp.route("/users", methods=['GET'])
def users():
    user = User()
    all_users = user.getUsers()
    return jsonify(dumps(all_users))


@bp.route("/companies", methods=['GET'])
def companies():
    company = Company()
    all_companies = company.getCompanies()
    return jsonify(dumps(all_companies))


@bp.route("/login/user", methods=['Get', 'POST'])
def login_user():
    if request.method == 'POST':
        try:
            user_details = request.json['user']
        except:
            return jsonify('Invalid data given'), 400
        email = user_details['email']
        password = user_details['password']
        if email is None:
            return jsonify({"msg": 'Email is required'}), 400
        elif password is None:
            return jsonify({"msg": 'Password is required'}), 400
        else:
            user = User()
            res = user.authenticateUser(email, password)
            return jsonify(res)
    return jsonify('')


@bp.route("/login/company", methods=['Get', 'POST'])
def login_company():
    if request.method == 'POST':
        try:
            company_details = request.json['company']
        except:
            return jsonify('Invalid data given'), 400
        email = company_details['email']
        password = company_details['password']
        if email is None:
            return jsonify({"msg": 'Email is required'}), 400
        elif password is None:
            return jsonify({"msg": 'Password is required'}), 400
        else:
            company = Company()
            res = company.authenticateCompany(email, password)
            return jsonify(res)
    return jsonify('')


@bp.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
