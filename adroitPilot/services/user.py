from bson.objectid import ObjectId

from .auth import EntityType, PersonServices
import shutil
from adroitPilot import app
import os

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


    def delete_resume(self, user_id, resume):
        user_details = self.db.read_one({'_id': ObjectId(user_id)})
        for i in range(len(user_details["resume"])):
            if user_details["resume"][i] == resume:
                del user_details["resume"][i]
                break

        try:
            arr = resume.split("/")
            directory_loc = arr[2].split("\\")[0]

            root_dir = os.path.dirname(app.instance_path)
            resume_directory = os.path.join(root_dir, app.config['UPLOAD_FOLDER'].split("./")[1], directory_loc)
            shutil.rmtree(resume_directory)
        except Exception as err:
            return str(err)
        self.db.replace({'_id': ObjectId(user_id)}, user_details)
        return True


    def checkIfExists(self, arr, keyword):
        for keyword_a in arr:
            if keyword_a.lower().strip() == keyword.lower().strip():
                return True

    def insert_keywords(self, user_id, keywords = []):
        user = self.db.read_one({'_id': ObjectId(user_id)})

        if "keywords" in user:
            keywords_list = []
            for keyword in keywords:
                keywords_list.append(keyword.lower())
            keywords_list = set(keywords_list)
            for keyword_l in keywords_list:
                user["keywords"].append(keyword_l)
        else:
            user["keywords"] = list(set(keywords))

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

