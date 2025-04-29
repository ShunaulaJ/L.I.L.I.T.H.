from langchain.schema import HumanMessage
from Agents.Workflow import APP
from Agents.States import *
from Agents.ToolKit import Tools
import os

class AppCoordinator:
    def __init__(self, APP, state, tools):
        """
        Initialize the backend logic.
        :param APP: The workflow application instance.
        :param state: The application state.
        :param tools: Utility tools for processing.
        """
        self.APP = APP
        self.state: State = state
        self.tools: Tools = tools

    def invoke_APP(self):
        """
        Invoke the workflow application with the current state.
        """
        self.state = self.APP.invoke(self.state)
        print("******* STATE: ******")
        print(self.state)

    def get_pretty_chat_history(self) -> str:
        """
        Retrieve the chat history as a string.
        :return: A string representation of the chat history.
        """
        return "\n".join([msg.content for msg in self.state["messages"]])

    # We'll test def value 
    def send_text(self, text: str = "ERROR: DEFAULT_VALUE") -> str:
        """
        Process text input and update the state.
        :param text: The text input from the user.
        :return: The updated chat history as a string.
        """
        print("********************  SENDING MSG  ********************")
        print(text)
        self.state["messages"].append(HumanMessage(content=text))
        self.invoke_APP()
        return self.get_pretty_chat_history()

    def send_audio(self, file: str) -> str:
        """
        Process audio input, transcribe it, and update the state.
        :param file: The file path of the audio input.
        :return: The updated chat history as a string.
        """
        print("********************  SENDING AUDIO  ********************")
        if not file or not os.path.exists(file):
            raise FileNotFoundError("No valid audio file provided.")

        # Transcribe the audio file to text
        transcription = self.tools.get_tts(file=file)
        print(f"Transcribed Text: {transcription}")

        # Add the transcription to the state
        self.state["messages"].append(HumanMessage(content=transcription))
        self.invoke_APP()
        return self.get_pretty_chat_history()