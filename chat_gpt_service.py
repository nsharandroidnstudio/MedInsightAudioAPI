import openai
import os

class ChatGPTService:
    def __init__(self, api_key=None):
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = "sk-" + os.getenv("OPENAI_API_KEY")


    def communicate_with_chatgpt(self,input_transcription):
        try:
            input_transcription = str(input_transcription)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content":f"Analyse the text.Output in one line just the false facts and their corrections.again in one line output only false facts and their corrections:"f" {input_transcription}"""
                },

                
                ],temperature=0.55
            )
            return response['choices'][0]['message']['content'].replace(r'\\n', '\n')
        except Exception as e:
            print(f"Error running generated code! Error: {e}")
            return None
