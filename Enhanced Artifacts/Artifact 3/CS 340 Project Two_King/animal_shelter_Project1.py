from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId

class AnimalShelter(object):
    # CRUD operations for Animal collection in MongoDB

    def __init__(self):
        # Connection Variables
        USER = 'aacuser'
        PASS = 'Password1!'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32233
        DB = 'AAC'
        COL = 'animals'

        # Initialize Connection
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

    # ENHANCEMENT: Input validation for data insertion
    # Ensures that only valid dictionaries are inserted into the database
    def create(self, data):
        if isinstance(data, dict) and data:
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged
            except Exception as e:
                print(f"Error inserting data: {e}")
                return False
        else:
            raise ValueError("Invalid input: Data must be a non-empty dictionary")

    # Reads documents from the collection based on a query
    # Returns all matching documents or all documents if no query is provided
    def read(self, query=None):
        try:
            cursor = self.collection.find(query or {}, {"_id": False})
            return list(cursor)
        except Exception as e:
            print(f"Error querying data: {e}")
            return []

    # Updates documents in the collection
    # Allows single or multiple updates based on the query parameters
    def update(self, query, new_values, update_many=False):
        if query and new_values:
            try:
                if update_many:
                    result = self.collection.update_many(query, {"$set": new_values})
                else:
                    result = self.collection.update_one(query, {"$set": new_values})
                return result.modified_count
            except Exception as e:
                print(f"Error updating data: {e}")
                return 0
        else:
            raise ValueError("Query and new_values must not be empty")

    # Deletes documents based on the provided query
    # Allows single or multiple deletions depending on the parameter
    def delete(self, query, delete_many=False):
        if query:
            try:
                if delete_many:
                    result = self.collection.delete_many(query)
                else:
                    result = self.collection.delete_one(query)
                return result.deleted_count
            except Exception as e:
                print(f"Error deleting data: {e}")
                return 0
        else:
            raise ValueError("Query must not be empty")

    # ENHANCEMENT: Index creation for improved performance
    # Creates an index on a specified field to optimize queries
    def optimize(self, field_name):
        if isinstance(field_name, str) and field_name:
            try:
                self.collection.create_index([(field_name, ASCENDING)])
                print(f"Index created on {field_name}")
            except Exception as e:
                print(f"Error creating index: {e}")
        else:
            raise ValueError("Invalid input: Field name must be a non-empty string")