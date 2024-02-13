import logging
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from MedicalRecord import MedicalRecord
from VoiceParser import VoiceParser
from chat_gpt_service import ChatGPTService
import re
from db_service import MongoDBHandler
newline_pattern = re.compile(r'\n')
app = FastAPI()
voice_parser = VoiceParser()
chat_gpt = ChatGPTService()
database = MongoDBHandler("SoundHealthDB")
@app.post("/upload_voice_data")
async def upload_voice_data(file: UploadFile = Form(...) ,user_key: str = Form(...) ,doctor_id:str =Form(...), patient_id:str =Form(...)):
    try:
        if not database.user_exists(user_key):
            return JSONResponse(content={"error": "not valid userkey!"})

        # Read the audio data from the uploaded file
        wav_data = await file.read()
        # Transcribe the WAV audio data using VoiceParser
        transcription = voice_parser.transcribe_wav_data(wav_data)
        logger.info(f"transcription:\n {transcription}")
        chat_analysis = chat_gpt.communicate_with_chatgpt(transcription)
        chat_analysis = newline_pattern.sub(' ', chat_analysis)
        medical_record = MedicalRecord(user_key,doctor_id,patient_id,transcription,chat_analysis)
        database.insert_user_data(medical_record)
        logger.info(f"Server answer {chat_analysis}")
        return JSONResponse(content={"Treatment recommendations: ": chat_analysis})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)

#Yoav, you need to implment a route that recive user_id and return all patient converstions meaning audio_transcription and chat analysis.
# If the user was not exists you will return Error, user id was not found.     
@app.get("/Get_patient_converstions")
async def upload_voice_data(patient_id:str =Form(...)):
    pass


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start the server and log a message
if __name__ == "__main__":
    import uvicorn

    # You can customize the host and port as needed
    host = "127.0.0.1"
    port = 8000

    uvicorn.run(app, host=host, port=port, debug=True)
    logger.info(f"Server is online at http://{host}:{port}")
