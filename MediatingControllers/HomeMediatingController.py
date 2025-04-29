import os
import traceback

class HomeMediatingController:
    def __init__(self, backend):
        """
        Initialize the controller with a backend instance.
        :param backend: An instance of the backend logic (e.g., RunApp).
        """
        self.backend = backend

    def process_text_input(self, text: str) -> str:
        """
        Process text input from the frontend.
        :param text: The text input from the user.
        :return: The updated chat history as a string.
        """
        if not text or not text.strip():
            return "Error: Text input cannot be empty."

        try:
            # Send text to the backend and get the updated chat history
            chat_history = self.backend.send_text(text)
            return chat_history
        except Exception as e:
            print(f"Error in process_text_input: {e}")
            return f"Error: {e}"

    def process_audio_input(self, file) -> str:
        """
        Process audio input from the frontend.
        :param file: The file path of the audio input or audio data.
        :return: The updated chat history as a string.
        """
        try:
            print(f"Audio input received: {file} (type: {type(file)})")
            
            # Handle different types of audio inputs
            if isinstance(file, str):
                # Direct file path
                audio_path = file
            elif isinstance(file, tuple) and len(file) >= 1:
                # Format: (file_path, sample_rate)
                audio_path = file[0]
            elif isinstance(file, dict) and 'path' in file:
                # Gradio format with path in dict
                audio_path = file['path']
            else:
                return "Error: Received unsupported audio format"
                
            print(f"Using audio path: {audio_path}")
            
            if not audio_path or not os.path.exists(audio_path):
                return "Error: No valid audio file provided"
                
            # Send audio to the backend and get the updated chat history
            chat_history = self.backend.send_audio(audio_path)
            return chat_history
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error in process_audio_input: {e}")
            print(f"Traceback: {error_details}")
            return f"Error: {str(e)}"
