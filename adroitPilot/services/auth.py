from werkzeug.security import check_password_hash, generate_password_hash
from . import DatabaseRepository
from flask_jwt_extended import create_access_token


class User:
    def registerService(self, user_details):
        email = user_details['email']
        password = user_details['password']
        error = None
        if email is None:
            error = 'Email is required'
        elif password is None:
            error = 'Password is required'
        else:
            db = DatabaseRepository('users')
            if db.read_one({'email': email}) is None:
                user_details['password'] = generate_password_hash(password)
                db.create(user_details)
                return {'result': 'success'}
            else:
                error = 'Email exists'

        return {'result': error}

    def getUsers(self):
        db = DatabaseRepository('users')
        users = db.read()
        all_users = []
        if users is not None:
            for user in users:
                all_users.append(user)
            return {'users': all_users}
        else:
            return {'users': ''}

    def authenticate(self, email, password):
        db = DatabaseRepository('users')
        user = db.read_one({'email': email})
        error = None
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            access_token = create_access_token(identity=email)
            return {'msg': 'success', 'access_token': access_token}
        else:
            return {'msg': error}
