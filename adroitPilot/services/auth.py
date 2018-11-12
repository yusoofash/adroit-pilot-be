from werkzeug.security import check_password_hash, generate_password_hash
from . import DatabaseRepository
from flask_jwt_extended import create_access_token


class PersonServices:
    def registerService(self, user_details, db):
        userDetails = user_details
        error = None
        if 'email' not in userDetails:
            return 'Email is required'
        elif 'password' not in userDetails:
            return 'Password is required'
        else:
            email = userDetails['email']
            pno = None
            company_name = None
            password = userDetails['password']
            if db.read_one({'email': email}) is not None:
                return 'Email exists'
            elif 'contact_no' in userDetails:
                pno = userDetails['pno']
                if db.read_one({'contact_no': pno}) is not None:
                    return 'Phone no. exists'
            elif 'company_name' in userDetails:
                company_name = userDetails['company_name']
                if db.read_one({'company_name': company_name}) is not None:
                    return 'Company name exists'

            user_details['password'] = generate_password_hash(password)
            db.create(user_details)
            return 'success'

    def getPeople(self, db):
        users = db.read()
        all_users = []
        if users is not None:
            for user in users:
                all_users.append(user)
            return all_users
        else:
            return ''

    def authenticate(self, email, password, db):
        user = db.read_one({'email': email})
        error = None
        if user is None:
            # error = 'Incorrect username'
            error = 'Incorrect email or password'
        elif not check_password_hash(user['password'], password):
            # error = 'Incorrect password'
            error = 'Incorrect email or password'

        if error is None:
            access_token = create_access_token(identity=email)
            return {'msg': 'success', 'access_token': access_token}
        else:
            return {'msg': error}


class User(PersonServices):
    def get_db(self):
        db = DatabaseRepository('user')
        return db

    def registerUser(self, user_details):
        db = self.get_db()
        return self.registerService(user_details, db)

    def getUsers(self):
        db = self.get_db()
        return self.getPeople(db)

    def authenticateUser(self, email, password):
        db = self.get_db()
        return self.authenticate(email, password, db)


class Company(PersonServices):
    def get_db(self):
        db = DatabaseRepository('company')
        return db

    def registerCompany(self, company_details):
        db = self.get_db()
        return self.registerService(company_details, db)

    def getCompanies(self):
        db = self.get_db()
        return self.getPeople(db)

    def authenticateCompany(self, email, password):
        db = self.get_db()
        return self.authenticate(email, password, db)
