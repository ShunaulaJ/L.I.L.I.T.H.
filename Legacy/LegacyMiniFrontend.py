from langchain.schema import HumanMessage
from Workflow import APP
from States import *
from ToolKit import Tools
import gradio as gr
import os

# TODO: Create logger for the app 

class RunApp:
    def __init__(self, APP, state, tools):
        self.APP = APP
        self.state: State = state
        self.tools: Tools = tools
    
    def invoke_APP(self):
        self.state = self.APP.invoke(self.state)
        print("******* STATE: ******")
        print(self.state)
    
    def get_chat_history(self):
        # Return a string showing the conversation history
        return "\n".join([msg.content for msg in self.state["messages"]])
    
    def send_text(self, text):
        print("********************  SENDING MSG  ********************")
        print(text)
        self.state["messages"].append(HumanMessage(content=text))
        self.invoke_APP()
        return self.get_chat_history()
    
    def send_audio(self, audio):
        print("********************  SENDING AUDIO  ********************")
        # # Validate the file path 
        # if not audio or not os.path.exists(audio):
        #     print("Error: No valid audio file provided.")
        #     return "Error: No valid audio file provided."
        # # print(audio)
        # # transcription = self.tools.get_tts(file=audio)
        # # self.state["messages"].append(HumanMessage(content=transcription))
        # # self.invoke_APP()
        return self.get_chat_history()


if __name__ == "__main__":

    app = APP
    state: State = {"messages": []}
    tools = Tools()
    runApp = RunApp(APP=app, state=state, tools=tools)

    # UI Components
    with gr.Blocks() as demo:
        gr.Markdown("# Welcome to L.I.L.I.T.H.")
        gr.Markdown("This is a simple chat interface. Below is the chat history:")

        with gr.Row():
            text_input = gr.Textbox(placeholder="say hey!", label="Input Text")
            text_submit_button = gr.Button("Send")

        audio_input = gr.Audio(type="filepath", label="Input Audio")
        audio_submit_button = gr.Button("Send Audio")

        state_log_display = gr.Textbox(label="Chat History", lines=10, interactive=False)
        
        # UI Logic
        text_submit_button.click(runApp.send_text, inputs=text_input, outputs=state_log_display)
        
        # TODO: THIS IS CAUSING AN ERROR 
        audio_submit_button.click(runApp.send_audio, inputs=audio_input, outputs=state_log_display)

    demo.launch()
