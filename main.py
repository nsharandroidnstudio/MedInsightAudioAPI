import logging
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from VoiceParser import VoiceParser
from chat_gpt_service import ChatGPTService
import re
from db_service import MongoDBHandler
newline_pattern = re.compile(r'\n')
app = FastAPI()
voice_parser = VoiceParser()
chat_gpt = ChatGPTService()
database = MongoDBHandler("true_gurad_db")
@app.post("/upload_voice_data")
async def upload_voice_data(file: UploadFile = Form(...),userkey: str = Form(...),audio_name:str =Form(...) ):
    try:
        if not database.user_exists(userkey, "users"):
            return JSONResponse(content={"error": "not valid userkey!"})

        # Read the audio data from the uploaded file
        wav_data = await file.read()
        # Transcribe the WAV audio data using VoiceParser
        transcription = voice_parser.transcribe_wav_data(wav_data)
        logger.info(f"transcription:\n {transcription}")
        # Assuming you have a function communicate_with_chatgpt to interact with ChatGPT
        answer = chat_gpt.communicate_with_chatgpt(transcription)
        new_answer = newline_pattern.sub(' ', answer)
        logger.info(f"Server answer {new_answer}")
        return JSONResponse(content={"transcription": transcription, "chat_response": new_answer})

    except HTTPException as http_exception:
        return JSONResponse(content={"error": f"HTTPException: {str(http_exception)}"}, status_code=http_exception.status_code)
    except Exception as general_exception:
        return JSONResponse(content={"error": f"Unexpected error: {str(general_exception)}"}, status_code=500)


@app.get("/Get_user_")




# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start the server and log a message
if __name__ == "__main__":
    import uvicorn

    # You can customize the host and port as needed
    host = "127.0.0.1"
    port = 8000

    uvicorn.run(app, host=host, port=port)
    logger.info(f"Server is online at http://{host}:{port}")
