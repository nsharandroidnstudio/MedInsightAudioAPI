
import speech_recognition as sr
import io

class VoiceParser:
     
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.file_transcription = None

    def transcribe_wav_data(self, wav_data):
        try:
            with sr.AudioFile(io.BytesIO(wav_data)) as audio_file:
                audio_data = self.recognizer.record(audio_file)
                try:
                    self.file_transcription = self.recognizer.recognize_google(audio_data)
                    return self.file_transcription
                except sr.UnknownValueError:
                    return "Speech Recognition could not understand audio"
                except sr.RequestError as e:
                    return "Could not request results from Google Web Speech API; {0}".format(e)
        except sr.AudioFileError as e:
            return "Error opening audio file: {0}".format(e)
        except sr.RequestError as e:
            return "Error processing audio file: {0}".format(e)



