from openai import OpenAI
import os

class Tools:
    def __init__(self):
        # TODO: Maybe make a seperate file for senstive data calling. currently we're just grabbing it from Tools.. prob not the best
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
        self.whisper_client = OpenAI(api_key=self.api_key)
    

    # TODO: Going to need to have it accept input for audio
    def get_tts(self, file: str = "audio_test.m4a") -> str:
        """
        This is a tool that takes an audio file and returns the text transcription. 
        """
        
        # TODO: Add a check here for error handling
        audio_file = open(file, "rb")
        transcription = self.whisper_client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=audio_file)

        return transcription.text