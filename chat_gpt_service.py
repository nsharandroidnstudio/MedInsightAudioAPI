from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


class ChatGPTService:

    def communicate_with_chatgpt(self, input_transcription):

        input_transcription = str(input_transcription)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"I am a doctor. Here is conversation between me and my patient: \n{input_transcription}\nWhat alternative tests are recommended to the patient to do? list shortly only 3 tests. Don't write anything else, just the 3 tests. Please also explain in one sentence each of the 3 tests. In addition, the tests should be specific. For example, complete blood count in not a specific test"
                }
            ],
            model="gpt-3.5-turbo",
            stream=True,
        )
        result = ""
        for chunk in chat_completion:
            if chunk.choices[0].delta.content is not None:
                result += chunk.choices[0].delta.content
        return result