#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'Password1!'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32233
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        # Creates a new document in the collection
        
        if data is not None:
            try:
                # Inserts the data into the collection
                result = self.collection.insert_one(data)
                return result.acknowledged  # Returns True if insert was acknowledged
            except Exception as e:
                print(f"Error inserting data: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def read(self, query=None):
        # Reads documents from the collection based on a query
        
        try:
            if query is not None:
                # Finds documents matching the query
                cursor = self.collection.find(query, {"_id": False})
            else:
                # Finds all documents if no query is passed
                cursor = self.collection.find({}, {"_id": False})

            # Converts cursor to list of documents
            result = [document for document in cursor]
            return result

        except Exception as e:
            print(f"Error querying data: {e}")
            return []
        
    def update(self, query, new_values, update_many=False):
        # Updates documents in the collection based on a query
        
        if query is not None and new_values is not None:
            try:
                if update_many:
                    # Updates all documents that match the query
                    result = self.collection.update_many(query, {"$set": new_values})
                else:
                    #Updates the first document that matches the query
                    result = self.collection.update_one(query, {"$set": new_values})
                return result.modified_count  # Returns the number of documents modified
            except Exception as e:
                print(f"Error updating data: {e}")
                return 0
        else:
            raise Exception("Nothing to update, query and new_values parameters must not be empty")
            
    def delete(self, query, delete_many=False):
        # Deletes documents from the collection based on a query
        
        if query is not None:
            try:
                if delete_many:
                    # Deletes all the documents that match the query
                    result = self.collection.delete_many(query)
                else:
                    # Deletes the first document that matches the query
                    result = self.collection.delete_one(query)
                return result.deleted_count  # Returns the number of documents deleted
            except Exception as e:
                print(f"Error deleting data: {e}")
                return 0
        else:
            raise Exception("Nothing to delete, query parameter must not be empty")       

