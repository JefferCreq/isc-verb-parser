# Run this file to test the MongoDB operations (CRUD) using Python's unittest module
# Run the tests using the following command:
# python -m unittest db/mongodb_test_operations.py

import unittest
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class TestMongoDBOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        username = os.getenv('MONGO_USERNAME')
        password = os.getenv('MONGO_PASSWORD')
        cluster_url = os.getenv('MONGO_CLUSTER_URL')

        uri = f"mongodb+srv://{username}:{password}@{cluster_url}"

        cls.client = MongoClient(
            uri + '/iskonawa_db?retryWrites=true&w=majority')
        cls.db = cls.client['iskonawa_db']
        cls.collection = cls.db['verbs']

    def setUp(self):
        # Data used for testing
        self.verb_data = {
            "verb": "test_verb",
            "spanish_meaning": "prueba",
            "english_meaning": "test",
            "inflected_forms": [{
                "index": "1",
                "iskonawa_sentence": "test sentence",
                "suffix_sentence": "test-suffix",
                "annotated_sentence": "test-annotated",
                "spanish_sentence": "frase de prueba",
                "reference": "test-reference",
                "key": "T1",
                "POS": "NOUN",
                "spanish_verbs": ["comer"],
                "verb_abbreviations": "comer-PERF",
                "verb_features": ["PERF"],
                "iskonawa_verb_segmented": "test-segmented",
                "iskonawa_verb": "test",
                "dict_verb": "test_verb"
            }]
        }

    def test_insert_verb(self):
        # Insert a verb into MongoDB
        result = self.collection.insert_one(self.verb_data)
        inserted_id = result.inserted_id

        # Assert that the insertion was successful
        self.assertIsNotNone(inserted_id)

        # Check if the inserted document exists in the collection
        inserted_verb = self.collection.find_one(
            {"_id": ObjectId(inserted_id)})
        self.assertIsNotNone(inserted_verb)
        self.assertEqual(inserted_verb['verb'], 'test_verb')

    def test_modify_verb(self):
        # Insert the verb first
        result = self.collection.insert_one(self.verb_data)
        inserted_id = result.inserted_id

        # Modify the inserted verb's meaning
        new_spanish_meaning = "prueba_modificada"
        self.collection.update_one({"_id": ObjectId(inserted_id)}, {
                                   "$set": {"spanish_meaning": new_spanish_meaning}})

        # Fetch the updated verb
        updated_verb = self.collection.find_one({"_id": ObjectId(inserted_id)})

        # Assert that the update was successful
        self.assertEqual(updated_verb['spanish_meaning'], new_spanish_meaning)

    def test_view_verb(self):
        # Insert the verb first
        result = self.collection.insert_one(self.verb_data)
        inserted_id = result.inserted_id

        # Retrieve (view) the inserted verb from MongoDB
        viewed_verb = self.collection.find_one({"_id": ObjectId(inserted_id)})

        # Assert that the verb can be retrieved and that the data matches
        self.assertIsNotNone(viewed_verb)
        self.assertEqual(viewed_verb['verb'], 'test_verb')
        self.assertEqual(viewed_verb['spanish_meaning'], 'prueba')
        self.assertEqual(viewed_verb['english_meaning'], 'test')

    def test_delete_verb(self):
        # Insert the verb first
        result = self.collection.insert_one(self.verb_data)
        inserted_id = result.inserted_id

        # Delete the inserted verb
        delete_result = self.collection.delete_one(
            {"_id": ObjectId(inserted_id)})

        # Assert that the deletion was successful
        self.assertEqual(delete_result.deleted_count, 1)

        # Check if the document no longer exists in the collection
        deleted_verb = self.collection.find_one({"_id": ObjectId(inserted_id)})
        self.assertIsNone(deleted_verb)

    @classmethod
    def tearDownClass(cls):
        # Clean up the test data
        # Clean up any test documents after the tests are complete
        cls.collection.delete_many({"verb": "test_verb"})
        cls.client.close()


if __name__ == '__main__':
    unittest.main()
