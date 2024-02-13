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

    def create_user_document(self, userkey, audio_file, transcription, chat_analysis):
        return {
            "userkey": userkey,
            "audio_file": audio_file,
            "audio_transcription": transcription,
            "chat_analysis": chat_analysis
        }

    def insert_user_data(self, userkey, audio_file, transcription, chat_analysis, collection_name):
        try:
            user_document = self.create_user_document(userkey, audio_file, transcription, chat_analysis)
            collection = self.db[collection_name]
            collection.insert_one(user_document)
        except Exception as e:
            print(f"Error inserting user data: {e}")

    def get_user_data(self, userkey, collection_name):
        try:
            collection = self.db[collection_name]
            return collection.find_one({"userkey": userkey})
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    def user_exists(self, userkey, collection_name):
        try:
            collection = self.db[collection_name]
            return collection.find_one({"userkey": userkey}) is not None
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False

# Example usage outside the class
"""
if __name__ == "__main__":
    db_handler = MongoDBHandler("true_gurad_db")

    userkey = "123"
    audio_file = "example_audio.wav"
    transcription = "This is a sample transcription."
    chat_analysis = "Sample chat analysis results."

    db_handler.insert_user_data(userkey, audio_file, transcription, chat_analysis, "users")

    # Check if user exists
    if db_handler.user_exists(userkey, "users"):
        print(f"User with userkey '{userkey}' exists.")
    else:
        print(f"User with userkey '{userkey}' does not exist.")

    db_handler.print_entire_db_info("users")
"""
