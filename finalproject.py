import openai
import os

openai.api_key = "sk-" + os.getenv("OPENAI_API_KEY")

# Specify the path to your WAV file
def communicate_with_chatgpt(input_transcription):
    try:
        input_transcription = str(input_transcription)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content":f"Show me all the false facts in the next transcription.Your output is the false sentnce and his corrections\n"f" {input_transcription}\n.."""
            },

            
            ],temperature=0.55
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error running generated code! Error: {e}")
        return None



wav_file = r"C:\Users\Nir\Desktop\Ai programming hw\final project\test2.ogg"
import speech_recognition as sr

def transcribe_wav_file(file_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Load the audio file
    with sr.AudioFile(file_path) as audio_file:
        # Record the audio from the file
        audio_data = recognizer.record(audio_file)
        try:
            # Use the Google Web Speech API to perform speech-to-text
            transcription = recognizer.recognize_google(audio_data)
            print(transcription)
            answer = communicate_with_chatgpt(transcription)
            print("chat response\n: {}".format(answer))
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))

if __name__ == "__main__":
    # Replace 'your_wav_file.wav' with the path to your WAV file
    wav_file_path = r"C:\Users\Nir\Desktop\Ai programming hw\final project\cool  lie 2.wav"
    
    transcribe_wav_file(wav_file_path)



