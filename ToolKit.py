from openai import OpenAI
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from langchain_google_community import CalendarToolkit
from elevenlabs import play
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)
import os

class Tools:
    def __init__(self):
        load_dotenv()   # Load environment variables from .env file
        # TODO: Maybe make a seperate file for senstive data calling. currently we're just grabbing it from Tools.. prob not the best
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.elev_api_key = os.getenv("ELEVENLABS_API_KEY")
        #self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key and not self.elev_api_key:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        self.whisper_client = OpenAI(api_key=self.api_key)
        self.elev_client = ElevenLabs(api_key=self.elev_api_key)
        #self.google_client = CalendarToolkit(api_key=self.google_api_key)
    

    # TODO: Going to need to have it accept input for audio
    def get_tts(self, file: str = "audio_test.m4a") -> str:
        """
        This is a tool that takes an audio file and returns the text transcription. 
        """
        
        # TODO: Add a check here for error handling
        audio_file = open(file, "rb")
        transcription = self.whisper_client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=audio_file)

        return transcription.text
    
    def get_elev_voice(self, text: str = "I'm sorry, I lost my train of thought") -> str:
        """
        This is a tool that takes text, return human voice. 
        """
        audio = self.elev_client.text_to_speech.convert(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",
        )
        play(audio)

        return text
    
    # TODO: This may have to got oa whole other LLM process?? idk
    def get_calendar_event(self):
        """
        This is a tool that takes a calendar event and returns the text transcription. 
        """
        toolkit = CalendarToolkit()

        credentials = get_google_credentials(
        token_file="token.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        client_secrets_file="credentials.json",
        )
        api_resource = build_resource_service(credentials=credentials)
        toolkit = CalendarToolkit(api_resource=api_resource)



if __name__ == "__main__":
    tools = Tools()
    print(tools.get_tts())
    tools.get_elev_voice()

