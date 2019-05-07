from bson.objectid import ObjectId

from .auth import EntityType, PersonServices


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

    def search_query(self, search):
        users = self.get_users()
        filtered_users = []
        for user in users:
            if "keywords" in user:
                if self.checkIfExists(user["keywords"], search):
                    filtered_users.append(user)
                elif search.lower() in user["email"].lower():
                    filtered_users.append(user)
            elif search.lower() in user["email"].lower():
                filtered_users.append(user)
        return filtered_users

    def update_user_details(self, details):
        user = self.db.read_one({'_id': ObjectId(details["id"])})
        from werkzeug.security import generate_password_hash
        user["password"] = generate_password_hash(details["password"])
        user["first_name"] = details["firstName"]
        user["last_name"] = details["lastName"]

        self.update_details(ObjectId(details["id"]), user)

        email = user["email"]
        password = details["password"]

        return self.authenticate(email, password)


    def checkIfExists(self, arr, keyword):
        for keyword_a in arr:
            if keyword_a.lower() == keyword.lower():
                return True

    def insert_keywords(self, user_id, keywords):
        user = self.db.read_one({'_id': ObjectId(user_id)})

        if "keywords" in user:
            keywords_list = []
            for keyword in keywords:
                keywords_list.append(keyword.lower())
            keywords_list = set(keywords_list)
            for keyword_l in keywords_list:
                user["keywords"].append(keyword_l)
        else:
            user["keywords"] = dict(set(keywords))

        self.db.replace({'_id': ObjectId(user_id)}, user)

    def update_user_resume_details(self, user_id, details):
        user = self.db.read_one({'_id': ObjectId(user_id)})
        if user is None:
            return None
        else:
            # for key in details:
            #     user[key] = details[key]
            if "resume" in user:
                user["resume"].append(details)
            else:
                user["resume"] = [details]
            # del user["_id"]
            self.db.replace({"_id": ObjectId(user_id)}, user)

