
import uuid
from db_service import MongoDBHandler


class Validator:    
    
    def check_id(self, id, doctor_or_patient):
        if len(id) != 9:
            return f"the length of {doctor_or_patient}_id should be 9"
        if not id.isdigit():
            return f"{doctor_or_patient}_id should consists digits only"
        return "valid"
    
        
    def check_user_key(self, user_key):
        error_msg = ""        
        if len(user_key) < 8:
            error_msg = "the password must contain at least 8 characters"    
        
        if not any(char.isupper() for char in user_key):
            message = "the password must contain at least one uppercase letter"
            if (error_msg  == ""):
                error_msg = message
            else:
                error_msg = error_msg + "," + message    
        
        if not any(char.islower() for char in user_key):
            message = "the password must contain at least one lowercase letter"
            if (error_msg  == ""):
                error_msg = message
            else:
                error_msg = error_msg + "," + message           
        
        if not any(char.isdigit() for char in user_key):
            message = "the password must contain at least one digit"
            if (error_msg  == ""):
                error_msg = message
            else:
                error_msg = error_msg + "," + message
        
        if (error_msg != ""):
            return error_msg
        else:      
            return "valid"
    

    def check_insert_new_doctor(self, doctor_id, user_key):
        error_msg = ""

        message1 = self.check_id(doctor_id, "doctor")
        if (message1 != "valid"):
            error_msg = message1

        message2 = self.check_user_key(user_key)
        if (message2 != "valid"):
            if (error_msg == ""):
                error_msg = message2
            else:
                error_msg = error_msg + "," + message2
        
        if (error_msg != ""):
            return error_msg
        else:      
            return "valid"



    def check_uploaded_file(self, file):
        allowed_extensions = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']
        file_extension = file.filename.split('.')[-1].lower()              
        if (file_extension not in allowed_extensions):
            return f"the file type is not supported. The type should be one of the following types: {allowed_extensions}"
        
        max_size_bytes = 25 * 1024 * 1024  # Convert MB to bytes
        file_data = file.file.read()
        file_size = len(file_data)
        file.file.seek(0)        
        if (file_size > max_size_bytes):
            return "the file is over 25MB. Please upload a file which is limited to 25MB"
        else:
            return "valid"
    

    def check_conversation_id(self, conversation_id):
        isValid = False
        try:
            uuid_obj = uuid.UUID(conversation_id)            
            if (str(uuid_obj) == conversation_id):
                isValid = True
        except ValueError:            
            isValid = False            
        
        if (isValid == True):
            return "valid"
        else:
            return "the conversation id is not a valid uuid"
           

    
    def check_topic(self, topic):
        allowed_topics = ['Asthma', 'COVID-19', 'Alzheimer', 'Headache', 'Back pain', 'Muscle pain', 'toothache']               
        if (topic not in allowed_topics):
            return f"the topic is not supported. You should enter one of the following topics: {allowed_topics}"
        else:
            return "valid"
        
    

    def check_upload_voice_data(self, file, patient_id, topic):
        error_msg = ""

        message1 = self.check_uploaded_file(file)               
        if (message1 != "valid"):            
            error_msg = message1   
            
        message2 = self.check_id(patient_id, "patient")
        if (message2 != "valid"):            
            if (error_msg == ""):
                error_msg = message2
            else:
                error_msg = error_msg + "," + message2
        
        message3 = self.check_topic(topic)
        if (message3 != "valid"):
            if (error_msg == ""):
                error_msg = message3
            else:
                error_msg = error_msg + "," + message3
              

        if (error_msg != ""):                        
            return error_msg
        else:      
            return "valid"

    

  


