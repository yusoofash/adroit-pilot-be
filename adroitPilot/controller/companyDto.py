from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.utils import secure_filename
from ..services.company import Company
import cloudinary.uploader
from bson.json_util import dumps
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

company_api = Blueprint('company', __name__)


@company_api.route("/companies", methods=['GET'])
@jwt_required
def companies():
    company = Company()
    all_companies = company.get_companies()
    return dumps(all_companies)


@company_api.route("/company/<ObjectId:id>", methods=['GET'])
@jwt_required
def company_details(id):
    company = Company()
    company = company.get_company(id)
    return dumps(company)


@company_api.route("/company/<ObjectId:id>", methods=['PUT'])
@jwt_required
def update_company_details(id):
    if not request.json:
        return jsonify('No data supplied'), 400
    details = request.json
    company = Company()
    res = company.update_company_details(id, details)
    return dumps(res)


@company_api.route("/company/upload", methods=['POST'])
@jwt_required
def upload_image():
    try:
        file = request.files['file']
    except Exception:
        return jsonify("key error: 'file'"), 400
    try:
        res = cloudinary.uploader.upload(file, eager = [
              {"width": 400, "height": 300,
                  "crop": "pad"},
              {"width": 260, "height": 200,
                  "crop": "crop", "gravity": "north"}])
        return dumps(res)
    except Exception as err:
        return dumps('Error Uploading image')

