from flask_pymongo import PyMongo


class DatabaseRepository:
    mongo = PyMongo()

    def __init__(self, col=None):
        self.db = self.mongo.db
        if col is not None:
            self.col = col

    def read(self, val=None):
        if val is None:
            return self.db[self.col].find()
        return self.db[self.col].find(val)

    def read_one(self, val=None):
        if val is None:
            return self.db[self.col].find_one()
        return self.db[self.col].find_one(val)

    def create(self, val):
        self.db[self.col].insert_one(val)

    def update(self, filter, replacment):
        result = self.db[self.col].update_one(filter, replacment)
        return result

    def delete(self, filter):
        self.db[self.col].delete_one(filter)

