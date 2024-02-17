from openai import OpenAI


class VoiceParser:

    def transcribe_wav_data(self, audio_path):
        client = OpenAI()
        audio_file = open(audio_path, "rb")
        transcript = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )

        return transcript.text





