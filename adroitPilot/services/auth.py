from werkzeug.security import check_password_hash, generate_password_hash
from . import DatabaseRepository
from flask_jwt_extended import create_access_token
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt
)
from bson.json_util import dumps
from adroitPilot import jwt
from enum import Enum


class EntityType(Enum):
    user = 1
    company = 2


class PersonServices:
    collection = None

    def __init__(self, collection):
        self.db = DatabaseRepository(collection)
        PersonServices.collection = collection
        
    def register_service(self, user_details):
        user_details = user_details
        if 'email' not in user_details:
            return 'Email is required'
        elif 'password' not in user_details:
            return 'Password is required'
        else:
            email = user_details['email']
            password = user_details['password']
            if self.db.read_one({'email': email}) is not None:
                return 'Email exists'
            elif 'contact_no' in user_details:
                pno = user_details['pno']
                if self.db.read_one({'contact_no': pno}) is not None:
                    return 'Phone no. exists'
            elif 'company_name' in user_details:
                company_name = user_details['company_name']
                if self.db.read_one({'company_name': company_name}) is not None:
                    return 'Company name exists'

            user_details['password'] = generate_password_hash(password)
            self.db.create(user_details)
            return self.authenticate(user_details['email'], password)

    def get_entity(self, entity_id=None):
        if entity_id is None:
            users = self.db.read()
            all_users = []
            if users is not None:
                for user in users:
                    del user['password']
                    all_users.append(user)
                return all_users
            else:
                return all_users
        else:
            user = self.db.read_one({"_id": entity_id})
            if user is not None:
                del user["password"]
                return user
            else:
                return user

    @jwt.jwt_data_loader
    def add_claims_to_access_token(identity):
        if PersonServices.collection == 'company':
            roles = 'company'
        else:
            roles = 'user'

        return {
            'sub': identity,
            'roles': roles
        }

    def authenticate(self, email, password):
        user = self.db.read_one({'email': email})
        error = None

        if user is None:
            # error = 'Incorrect username'
            error = 'Incorrect email or password'
        elif not check_password_hash(user['password'], password):
            # error = 'Incorrect password'
            error = 'Incorrect email or password'

        if error is None:
            access_token = create_jwt(str(user["_id"]))
            user_data = dict(user)
            del user_data["password"]
            return {'msg': 'success', 'access_token': access_token, 'data': user_data}
        else:
            return {'msg': error}

    def update_details(self, detail_id, details):
        db_details = self.db.read_one({'_id': detail_id})
        if db_details is None:
            return None
        for key in details:
            db_details[key] = details[key]
        del db_details["_id"]
        self.db.replace({"_id": detail_id}, db_details)
        return db_details


class User(PersonServices):
    def __init__(self):
        user = EntityType.user.name
        super().__init__(user)

    def register_user(self, user_details):
        return self.register_service(user_details)

    def get_users(self):
        return self.get_entity()

    def get_user(self, user_id):
        return self.get_entity(user_id)

    def authenticate_user(self, email, password):
        return self.authenticate(email, password)

    def update_user_details(self, user_id, details):
        from bson.objectid import ObjectId
        user = self.db.read_one({'_id': ObjectId(user_id)})
        if user is None:
            return None
        else:
            # for key in details:
            #     user[key] = details[key]
            if "resume" in user:
                user["resume"].append(details)
            else:
                user["resume"] = details
            del user["_id"]
            self.db.replace({"_id": ObjectId(user_id)}, user)
            del user['password']
            return user
