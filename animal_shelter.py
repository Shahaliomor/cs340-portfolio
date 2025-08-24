from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Connection Variables
        USER = 'aacuser'
        PASS = 'omor123'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31630
        DB = 'AAC'
        COL = 'animals'

        try:
            # Initialize Connection
            self.client = MongoClient(
                'mongodb://%s:%s@%s:%d' % (username, password, HOST, PORT)
            )
            self.database = self.client[DB]
            self.collection = self.database[COL]
        except PyMongoError as e:
            raise Exception(f"Could not connect to MongoDB: {e}")

    def create(self, data):
        """ Insert a document into the collection """
        if data is None:
            raise Exception("Nothing to save, because data parameter is empty")
        try:
            result = self.collection.insert_one(data)
            return result.acknowledged
        except PyMongoError as e:
            raise Exception(f"Create failed: {e}")

    def read(self, query):
        """ Query for documents and return a list """
        if query is None:
            raise Exception("Nothing to search, because query parameter is empty")
        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError as e:
            raise Exception(f"Read failed: {e}")

    def update(self, query, update_values, many=False):
        """
        Update one or more documents.
        Returns number of documents modified.
        """
        if query is None or update_values is None:
            raise Exception("Update requires both query and update_values")
        try:
            update_op = {"$set": update_values}
            if many:
                result = self.collection.update_many(query, update_op)
            else:
                result = self.collection.update_one(query, update_op)
            return result.modified_count
        except PyMongoError as e:
            raise Exception(f"Update failed: {e}")

    def delete(self, query, many=False):
        """
        Delete one or more documents.
        Returns number of documents deleted.
        """
        if query is None:
            raise Exception("Delete requires a query parameter")
        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as e:
            raise Exception(f"Delete failed: {e}")

    def close(self):
        """ Close MongoDB connection """
        try:
            self.client.close()
        except PyMongoError as e:
            raise Exception(f"Error closing connection: {e}")
