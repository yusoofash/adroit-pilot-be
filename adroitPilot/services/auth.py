from werkzeug.security import check_password_hash, generate_password_hash
from . import DatabaseRepository


class User:
    def registerService(self, userDetails):
        email = userDetails['email']
        password = userDetails['password']
        error = None
        if email is None:
            error = 'Email is required'
        elif password is None:
            error = 'Password is required'
        else:
            db = DatabaseRepository('users')
            if db.read_one({'email': email}) is None:
                userDetails['password'] = generate_password_hash(password)
                db.create(userDetails)
                return {'result': 'success'}
            else:
                error = 'Email exists'

        return {'result': error}

    def getUsers(self):
        db = DatabaseRepository('users')
        users = db.read()
        if users is not None:
            return {'result': users}
        else:
            return {'result': ''}
