from fastapi import logger
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, database_name):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
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

    def create_user_document(self, user_key, doctor_id , patient_id ,transcription, chat_analysis):
        return {
            "user_key": user_key,
            "doctor_id":doctor_id,
            "patient_id":patient_id,
            "audio_transcription": transcription,
            "chat_analysis": chat_analysis
        }

    def insert_user_data(self, MedicalRecord , collection_name="patient_conversation"):
        try:
            user_document = self.create_user_document(MedicalRecord.user_key, MedicalRecord.doctor_id, MedicalRecord.patient_id, MedicalRecord.transcription, MedicalRecord.chat_analysis)
            collection = self.db[collection_name]
            collection.insert_one(user_document)
            
        except Exception as e:
            print(f"Error inserting user data: {e}")

    def get_user_data(self, userkey, collection_name="patient_conversation"):
        try:
            collection = self.db[collection_name]
            return collection.find_one({"userkey": userkey})
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    def user_exists(self, userkey, collection_name="patient_conversation"):
        try:
            collection = self.db[collection_name]
            return collection.find_one({"user_key": userkey}) is not None
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False
        

# Example usage outside the class

if __name__ == "__main__":
    db_handler = MongoDBHandler("SoundHealthDB")
    user_key = "123"
    doctor_id = None
    patient_id = None
    transcription = None
    chat_analysis = None

    #db_handler.insert_user_data(user_key, doctor_id, patient_id, transcription, chat_analysis)
    db_handler.print_entire_db_info("patient_conversation")
