from bson import ObjectId

from adroitPilot import mongo


class DatabaseRepository:

    def __init__(self, col):
        self.mongo = mongo
        try:
            self.db = self.mongo.db[col]
        except Exception as err:
            raise Exception('Collection not specified', err)

    def read(self, val=None, projection=None):
        if val is None:
            return self.db.find({})
        elif projection is not None:
            return self.db.find(val, projection)
        else:
            return self.db.find(val)

    def read_one(self, val=None):
        if val is None:
            return self.db.find_one({})
        return self.db.find_one(val)

    def create(self, val=None):
        if val is None:
            return None
        self.db.insert_one(val)

    def replace(self, filter1, replacment):
        result = self.db.replace_one(filter1, replacment)
        return result

    def delete(self, filter):
        self.db.delete_one(filter)

