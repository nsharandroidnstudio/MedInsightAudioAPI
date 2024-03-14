import logging
import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from MedicalRecord import MedicalRecord
from VoiceParser import VoiceParser
from chat_gpt_service import ChatGPTService
from Validator import Validator
import re
from db_service import MongoDBHandler
import uuid
from VectorDB import VectorDB

newline_pattern = re.compile(r'\n')
app = FastAPI()
voice_parser = VoiceParser()
chat_gpt = ChatGPTService()
database = MongoDBHandler("SoundHealthDB")
validator = Validator()
vector_db = VectorDB()

@app.post("/insert_new_doctor")
async def insert_new_doctor(user_key: str = Form(None) ,doctor_id:str =Form(None)):    
    message = validator.check_user_key_and_doctor_id(doctor_id, user_key)
    if (message != "valid"):
        return JSONResponse(content={"error": message}, status_code=400) 
                  
    if database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is already exist. Try again"}, status_code=400)
    
    database.insert_doctor_data(user_key, doctor_id)
    return JSONResponse(content={"message": "new doctor user created successfully"})
               
     
@app.post("/upload_voice_data")
async def upload_voice_data(file: UploadFile = Form(None) ,user_key: str = Form(None) ,doctor_id:str =Form(None), patient_id:str =Form(None), topic:str =Form(None)):   
    try:        
        message = validator.check_upload_voice_data(file, user_key, doctor_id, patient_id, topic)
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        # Save the audio file locally
        try:
            upload_folder = "./"
            fileName = "temp_" + file.filename
            audio_path = os.path.join(upload_folder, fileName)            
            with open(audio_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving file: {e}")         

        transcription = voice_parser.transcribe_wav_data(audio_path)           
                                 
        chat_analysis = chat_gpt.communicate_with_chatgpt(transcription)
        chat_analysis = newline_pattern.sub(' ', chat_analysis)
        generated_id = uuid.uuid4()
        conversation_id = str(generated_id)
        medical_record = MedicalRecord(user_key, doctor_id, patient_id, topic, conversation_id, transcription, chat_analysis)
        database.insert_user_data(medical_record)
        vector_db.insert_document(conversation_id, topic + chat_analysis)

        # Delete the temporary audio file
        try:
            os.remove(audio_path)
        except OSError as e:
            print(f"Error deleting temporary file: {e}")

        return JSONResponse(content={"Treatment recommendations: ": chat_analysis, "conversation id:": conversation_id})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)
   
@app.get("/get_patient_conversations")
async def get_patient_conversations(user_key: str = Form(None), doctor_id:str =Form(None), patient_id:str =Form(None)):
    try:        
        message = validator.check_get_patient_conversations(user_key, doctor_id, patient_id)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400)
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400) 
               
        conversations = database.get_conversations_by_element(patient_id, "patient_id")
        return JSONResponse(content={"conversations: ": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_doctor_conversations")
async def get_doctor_conversations(user_key: str = Form(None), doctor_id:str =Form(None)):
    try:
        message = validator.check_user_key_and_doctor_id(doctor_id, user_key)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400)
                
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations = database.get_all_doctor_conversations(user_key, doctor_id)
        return JSONResponse(content={"conversations: ": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_topic_conversations")
async def get_topic_conversations(user_key: str = Form(None), doctor_id:str =Form(None), topic:str =Form(None)):
    try:
        message = validator.check_get_topic_conversations(user_key, doctor_id, topic)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
              
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations = database.get_conversations_by_element(topic, "topic")
        return JSONResponse(content={"conversations: ": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_id_conversations")
async def get_id_conversations(user_key: str = Form(None), doctor_id:str =Form(None), conversation_id:str =Form(None)):
    try:
        message = validator.check_user_key_and_doctor_id_and_conversation_id(user_key, doctor_id, conversation_id)
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations = database.get_conversations_by_element(conversation_id, "conversation_id")
        return JSONResponse(content={"conversations: ": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_similar_conversations")
async def get_similar_conversations(user_key: str = Form(None), doctor_id: str = Form(None),
                                    conversation_id: str = Form(None)):
    try:
        message = validator.check_user_key_and_doctor_id_and_conversation_id(user_key, doctor_id, conversation_id)
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)

        text = vector_db.get_text_by_conversation_id(conversation_id)

        if text is None:
            return JSONResponse(content={"error": "Conversation is not exist"}, status_code=400)

        result = vector_db.find_similar_conversions(text)
        return JSONResponse(result)

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred,please try later.."}, status_code=500)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start the server and log a message
if __name__ == "__main__":
    import uvicorn

    # You can customize the host and port as needed
    host = "127.0.0.1"
    port = 80

    uvicorn.run(app, host=host, port=port, debug=True)
    logger.info(f"Server is online at http://{host}:{port}")