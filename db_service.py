from fastapi import logger
from pymongo import MongoClient

from MedicalRecord import MedicalRecord


class MongoDBHandler:
    def __init__(self, database_name):
        try:
            self.client = MongoClient("mongodb://mongo:27017/")
            self.db = self.client[database_name]
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
    
    def print_entire_db_info(self, collection_name):
        try:
            collection = self.db[collection_name]
            all_documents = collection.find()

            print(f"Entire Information of {self.db.name}.{collection_name}:\n")
            for document in all_documents:
                print(document)
                print("------------------------")
        except Exception as e:
            print(f"Error printing entire DB info: {e}")

    def create_user_document(self, user_key, doctor_id, patient_id, topic, conversation_id, transcription,
                             chat_analysis):
        return {
            "user_key": user_key,
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "topic": topic,
            "conversation_id": conversation_id,
            "audio_transcription": transcription,
            "chat_analysis": chat_analysis
        }

    def create_doctor_document(self, user_key, doctor_id):
        return {
            "user_key": user_key,
            "doctor_id": doctor_id,
        }

    def insert_user_data(self, MedicalRecord, collection_name="patient_conversation"):
        try:
            user_document = self.create_user_document(MedicalRecord.user_key, MedicalRecord.doctor_id,
                                                      MedicalRecord.patient_id, MedicalRecord.topic,
                                                      MedicalRecord.conversation_id, MedicalRecord.transcription,
                                                      MedicalRecord.chat_analysis)
            collection = self.db[collection_name]
            collection.insert_one(user_document)

        except Exception as e:
            print(f"Error inserting user data: {e}")

    def insert_doctor_data(self, key, id, collection_name="doctor_users"):
        try:
            user_document = self.create_doctor_document(key, id)
            collection = self.db[collection_name]
            collection.insert_one(user_document)

        except Exception as e:
            print(f"Error inserting user data: {e}")

    def get_all_doctor_conversations(self, key, id, collection_name="patient_conversation"):
        try:
            collection = self.db[collection_name]
            return list(collection.find({"$and": [{"user_key": key}, {"doctor_id": id}]}, {"_id": 0}))
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None

    def user_exists(self, key, id, collection_name="doctor_users"):
        try:
            collection = self.db[collection_name]
            result = collection.find_one({"$and": [{"user_key": key}, {"doctor_id": id}]})
            return result is not None
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False

    def get_conversations_by_element(self, desired_value, element, collection_name="patient_conversation"):
        try:
            collection = self.db[collection_name]
            # collection = self.get_filtered_data(key, id)
            return list(collection.find({element: desired_value}, {"_id": 0}))
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []

   

