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
                    "content":f"I am a doctor. Here is conversation between me and my patient: \n{input_transcription}\nWhat alternative tests are recommended to the patient to do? list shortly only 3 tests. Don't write anything else, just the 3 tests. Please also explain in one sentence each of the 3 tests"
                },

                
                ]
            )
            return response['choices'][0]['message']['content'].replace(r'\\n', '\n')
        except Exception as e:
            print(f"Error running generated code! Error: {e}")
            return None
