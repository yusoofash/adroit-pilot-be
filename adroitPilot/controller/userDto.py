import os
import uuid
import logging
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, jsonify,
    send_from_directory, send_file)
from werkzeug.utils import secure_filename
from ..services.user import User
from ..services.company import Company
import cloudinary.uploader
from bson.json_util import dumps
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
from adroitPilot import app
import config

import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


user_api = Blueprint('user', __name__)


@user_api.route("/users", methods=['GET'])
@jwt_required
def users():
    user = User()
    all_users = user.get_users()
    return dumps(all_users)


@user_api.route("/user/resume_fetch/<path:path>", methods=['GET'])
def fetch_resume_user(path):
    arr = path.split("/")
    file_name = arr[len(arr)-1]
    directory_loc = arr[1]

    root_dir = os.path.dirname(app.instance_path)
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER'].split("./")[1], directory_loc), file_name)


@user_api.route("/user/<ObjectId:id>", methods=['PUT'])
@jwt_required
def update_company_details(id):
    if not request.json:
        return jsonify('No data supplied'), 400
    details = request.json
    user = User()
    res = user.get_user(id)
    return dumps(res)


@user_api.route("/user/<ObjectId:userid>", methods=['GET'])
@jwt_required
def user_details(userid):
    user = User()
    user = user.get_user(userid)
    return dumps(user)


@user_api.route("/user/update_account", methods=['POST'])
@jwt_required
def update_account():
    details = request.json['details']
    user = User()
    res = user.update_user_details(details)
    return dumps(res)


@user_api.route("/user/delete_resume", methods=['POST'])
@jwt_required
def delete_resume():
    user_id = request.json['id']
    # this path is used to delete the directory
    resume = request.json['resume']
    user = User()
    res = user.delete_resume(user_id, resume)
    return dumps(res)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


@user_api.route("/user/resume", methods=['POST'])
@jwt_required
def upload_resume():
    if request.method == 'POST':
        try:
            user_id = get_jwt_identity()
        except Exception as err:
            logging.exception(err)
            return dumps('Invalid user'), 400

        if 'file' not in request.files:
            return dumps('No selected file'), 400
        file = request.files['file']
        if file.filename == '':
            return dumps('No selected file'), 400
        if file and allowed_file(file.filename):
            new_directory = str(uuid.uuid1())
            filename = secure_filename(file.filename)
            file_directory = app.config['UPLOAD_FOLDER']+'/'+new_directory

            if filename.endswith('.pdf') or filename.endswith('.docx'):
                os.makedirs(file_directory)
                file_path = os.path.join(file_directory, filename)
                file.save(os.path.join(file_directory, filename))
                text = None
                if filename.endswith('.pdf'):
                    text = convert_pdf_to_txt(file_path)
                elif filename.endswith('.docx'):
                    import docx2txt
                    text = docx2txt.process(file_path)
                text_arr = text.split()

                all_text_arr = []

                for text_word in text_arr:
                    for word in text_word.split(","):
                        all_text_arr.append(word)

                text_arr = all_text_arr

                for i in range(len(text_arr)):
                    text_arr[i] = text_arr[i].lower()

                company = Company()
                matching_keywords = company.get_matching_keywords("keywords", text_arr)

                user = User()
                user.update_user_resume_details(user_id, file_path)

                user = User()
                user.insert_keywords(user_id, matching_keywords)

                company = Company()
                ranked_companies = company.rank_companies(text_arr)

                ranked_companies_flat = []
                for ranked_company in ranked_companies:
                    for company in ranked_company["companies"]:
                        ranked_companies_flat.append(company)

                return dumps(ranked_companies_flat)

            else:
                return dumps('Invalid file type'), 400
        return ''


@user_api.route('/user/resume_test', methods=['POST', 'GET'])
def upload_resume_test():
    if request.method == 'POST':
        try:
            user_id = get_jwt_identity()
        except Exception as err:
            logging.exception(err)
            return dumps('Invalid user'), 400

        if 'file' not in request.files:
            return dumps('No selected file'), 400
        file = request.files['file']
        if file.filename == '':
            return dumps('No selected file'), 400
        if file and allowed_file(file.filename):
            new_directory = str(uuid.uuid1())
            filename = secure_filename(file.filename)
            file_directory = app.config['UPLOAD_FOLDER']+'/'+new_directory

            if filename.endswith('.pdf') or filename.endswith('.docx'):
                os.makedirs(file_directory)
                file_path = os.path.join(file_directory, filename)
                file.save(os.path.join(file_directory, filename))
                text = None
                if filename.endswith('.pdf'):
                    text = convert_pdf_to_txt(file_path)
                elif filename.endswith('.docx'):
                    import docx2txt
                    text = docx2txt.process(file_path)
                text_arr = text.split()

                # user = User()
                # user.update_user_resume_details(user_id, file_path)

                company = Company()
                ranked_companies = company.rank_companies(text_arr)

                company = Company()
                matching_keywords = company.get_matching_keywords("keywords", text_arr)

                return dumps(matching_keywords)
            else:
                return dumps('Invalid file type'), 400
        return ''


@user_api.route('/user/resume/existing', methods=['POST'])
@jwt_required
def get_companies_from_resume():
    if not request.json:
        return dumps('No data given'), 400
    resume_path = request.json['resume_path']
    if resume_path.endswith('.pdf') or resume_path.endswith('.docx'):
        text = None
        if resume_path.endswith('.pdf'):
            text = convert_pdf_to_txt(resume_path)
        elif resume_path.endswith('.docx'):
            import docx2txt
            text = docx2txt.process(resume_path)
        text_arr = text.split()

        all_text_arr = []

        for text_word in text_arr:
            for word in text_word.split(","):
                all_text_arr.append(word)

        text_arr = all_text_arr

        company = Company()
        ranked_companies = company.rank_companies(text_arr)

        ranked_companies_flat = []
        for ranked_company in ranked_companies:
            for company in ranked_company["companies"]:
                ranked_companies_flat.append(company)

        return dumps(ranked_companies_flat)
    else:
        return dumps('Invalid file type'), 400
