import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from . import User
from bson.json_util import dumps
import json

bp = Blueprint('auth', __name__)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.json['user']
        user = User()
        res = user.registerService(userDetails)
        return jsonify(res)
    return jsonify('')


@bp.route("/users", methods=['GET'])
def users():
    user = User()
    all_users = user.getUsers()
    return jsonify(dumps(all_users))
