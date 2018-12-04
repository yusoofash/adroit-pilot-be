import os
import uuid
import logging
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.utils import secure_filename
from ..services.auth import User
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


@user_api.route("/user/<ObjectId:userid>", methods=['GET'])
@jwt_required
def user_details(userid):
    user = User()
    user = user.get_user(userid)
    return dumps(user)


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

                user = User()
                user.update_user_details(user_id, file_path)

                company = Company()
                companies = company.companies_matching_keywords(text_arr)

                return dumps(companies)
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

        company = Company()
        companies = company.companies_matching_keywords(text_arr)

        return dumps(companies)
    else:
        return dumps('Invalid file type'), 400
