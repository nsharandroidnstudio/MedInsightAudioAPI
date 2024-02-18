import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("config.env")
class VoiceParser:

    def transcribe_wav_data(self, audio_path):
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        audio_file = open(audio_path, "rb")
        transcript = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )

        return transcript.text





