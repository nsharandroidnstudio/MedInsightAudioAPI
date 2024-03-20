import logging
import os
from fastapi import FastAPI, UploadFile, Form, HTTPException, Query
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse
from MedicalRecord import MedicalRecord
from VoiceParser import VoiceParser
from chat_gpt_service import ChatGPTService
from Validator import Validator
import re
from db_service import MongoDBHandler
import uuid
from VectorDB import VectorDB
from stats import stats
from pydantic import BaseModel

newline_pattern = re.compile(r'\n')
app = FastAPI()
voice_parser = VoiceParser()
chat_gpt = ChatGPTService()
database = MongoDBHandler("SoundHealthDB")
validator = Validator()
vector_db = VectorDB()
statistics = stats()

class Content(BaseModel):
    content: str

@app.get("/", response_class=HTMLResponse)
async def get_home_page():
    with open("HomePage.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/HomePage.html", response_class=HTMLResponse)
async def get_home_page():
    with open("HomePage.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/outputPage.html", response_class=HTMLResponse)
async def get_output_page():
    with open("outputPage.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/styles.css")
def get_css():
    return FileResponse("styles.css")

@app.get("/doctor.png")
def get_doctor_image():
    return FileResponse("doctor.png")

@app.get("/RegisterPage.html", response_class=HTMLResponse)
async def get_register_page():
    with open("RegisterPage.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Upload_conversation.html", response_class=HTMLResponse)
async def get_upload_conversation_page():
    with open("Upload_conversation.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Patient_conversations.html", response_class=HTMLResponse)
async def get_patient_conversations_page():
    with open("Patient_conversations.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Doctor_conversations.html", response_class=HTMLResponse)
async def get_doctor_conversations_page():
    with open("Doctor_conversations.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Topic_conversations.html", response_class=HTMLResponse)
async def get_topic_conversations_page():
    with open("Topic_conversations.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/ID_conversation.html", response_class=HTMLResponse)
async def get_id_conversation_page():
    with open("ID_conversation.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Status_conversations.html", response_class=HTMLResponse)
async def get_status_conversations_page():
    with open("Status_conversations.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Similar_tests.html", response_class=HTMLResponse)
async def get_similar_tests_page():
    with open("Similar_tests.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Update_status.html", response_class=HTMLResponse)
async def get_update_status_page():
    with open("Update_status.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Statistics.html", response_class=HTMLResponse)
async def get_topic_statistics_page():
    with open("Statistics.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/Pie_charts.html", response_class=HTMLResponse)
async def get_topic_statistics_page():
    with open("Pie_charts.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

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
        medical_record = MedicalRecord(user_key, doctor_id, patient_id, topic, conversation_id, transcription, chat_analysis, "under review")
        database.insert_user_data(medical_record)
        vector_db.insert_document(conversation_id, topic + ": " + chat_analysis)

        try:
            os.remove(audio_path)
        except OSError as e:
            print(f"Error deleting temporary file: {e}")

        return JSONResponse(content={"Additional_medical_tests": chat_analysis, "conversation_id": conversation_id})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)
   
@app.get("/get_patient_conversations")
async def get_patient_conversations(user_key: str = Query(None), doctor_id:str = Query(None), patient_id:str = Query(None)):
    try:        
        message = validator.check_get_patient_conversations(user_key, doctor_id, patient_id)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400)
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400) 
               
        conversations, _ = database.get_conversations_by_element(patient_id, "patient_id")        
        return JSONResponse(content={"conversations": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_doctor_conversations")
async def get_doctor_conversations(user_key: str = Query(None), doctor_id:str =Query(None)):
    try:
        message = validator.check_user_key_and_doctor_id(doctor_id, user_key)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400)
                
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations = database.get_all_doctor_conversations(user_key, doctor_id)
        return JSONResponse(content={"conversations": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_topic_conversations")
async def get_topic_conversations(user_key: str = Query(None), doctor_id:str =Query(None), topic:str =Query(None)):
    try:
        message = validator.check_get_topic_conversations(user_key, doctor_id, topic)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
              
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations, _ = database.get_conversations_by_element(topic, "topic")
        return JSONResponse(content={"conversations": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_id_conversations")
async def get_id_conversations(user_key: str = Query(None), doctor_id:str =Query(None), conversation_id:str =Query(None)):
    try:
        message = validator.check_user_key_and_doctor_id_and_conversation_id(user_key, doctor_id, conversation_id)
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations, _ = database.get_conversations_by_element(conversation_id, "conversation_id")
        return JSONResponse(content={"conversations": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_status_conversations")
async def get_topic_conversations(user_key: str = Query(None), doctor_id:str =Query(None), status:str =Query(None)):
    try:
        message = validator.check_get_status_conversations(user_key, doctor_id, status)        
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
              
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        conversations, _ = database.get_conversations_by_element(status, "status")
        return JSONResponse(content={"conversations": conversations})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

@app.get("/get_similar_tests")
async def get_similar_conversations(user_key: str = Query(None), doctor_id: str = Query(None),conversation_id: str = Query(None)):
    try:
        message = validator.check_user_key_and_doctor_id_and_conversation_id(user_key, doctor_id, conversation_id)
        if (message != "valid"):
            return JSONResponse(content={"error": message}, status_code=400) 
        
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        _, id_length = database.get_conversations_by_element(conversation_id, "conversation_id")
        if id_length == 0:
            return JSONResponse(content={"error": "the conversation id is not exist"}, status_code=400)

        text = vector_db.get_text_by_conversation_id(conversation_id)

        if text is None:
            return JSONResponse(content={"error": "Conversation is not exist"}, status_code=400)

        result = vector_db.find_similar_conversions(text)
        return JSONResponse(result)

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred,please try later.."}, status_code=500)

@app.post("/update_status")
async def update_status(user_key: str = Form(None) ,doctor_id:str =Form(None), conversation_id:str =Form(None), status:str =Form(None)):  
    try:
        message = validator.check_update_status(user_key, doctor_id, conversation_id, status)
        if (message != "valid"):               
            return JSONResponse(content={"error": message}, status_code=400)         
                    
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
        
        _, id_length = database.get_conversations_by_element(conversation_id, "conversation_id")
        if id_length == 0:
            return JSONResponse(content={"error": "the conversation id is not exist"}, status_code=400)

        database.update_status(conversation_id, status)
        return JSONResponse(content={"message": "the status was updated successfully"})
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred,please try later.."}, status_code=500)

@app.get("/get_statistics")
async def get_statistics(user_key: str = Query(None), doctor_id:str =Query(None)):
    try:
        message = validator.check_user_key_and_doctor_id(doctor_id, user_key)
        if (message != "valid"):               
            return JSONResponse(content={"error": message}, status_code=400)         
                    
        if not database.user_exists(user_key, doctor_id):
            return JSONResponse(content={"error": "the user is not exist"}, status_code=400)
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred,please try later.."}, status_code=500)
    
    dictionary = {}    
    topic_dictionary = statistics.get_topic_statistics()
    status_dictionary = statistics.get_status_statistics()    
    topic_from_status_dictionary = statistics.get_topic_from_status_statistics()    
    dictionary.update(topic_dictionary)
    dictionary.update(status_dictionary)
    dictionary.update(topic_from_status_dictionary)

    return JSONResponse(content=dictionary) 

    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn

    host = "0.0.0.0"
    port = 80

    uvicorn.run(app, host=host, port=port, debug=True)
    logger.info(f"Server is online at http://{host}:{port}")