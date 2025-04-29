import sys
import os

# Add the project root directory to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from Controllers.HomeMediatingController import HomeMediatingController
from AppCoordinator import AppCoordinator
from ToolKit import Tools
from Workflow import APP
from States import State
import traceback

def safe_audio_handler(audio, controller):
    try:
        print(f"Audio received: {audio} (type: {type(audio)})")
        return controller.process_audio_input(audio)
    except Exception as e:
        print(f"Error processing audio: {e}")
        print(traceback.format_exc())
        return f"Error processing audio: {str(e)}"

if __name__ == "__main__":
    # Initialize backend and controller
    app = APP
    state: State = {"messages": []}
    tools = Tools()
    backend = AppCoordinator(APP=app, state=state, tools=tools)
    controller = HomeMediatingController(backend=backend)

    # UI Components
    with gr.Blocks() as demo:
        gr.Markdown("# Welcome to L.I.L.I.T.H.")
        gr.Markdown("This is a simple chat interface. Below is the chat history:")

        # Text Input Section
        with gr.Row():
            text_input = gr.Textbox(placeholder="say hey!", label="Input Text")
            text_submit_button = gr.Button("Send Text")

        # Audio Input Section
        with gr.Row():
            # Use compatible parameters for gr.Audio (without 'source')
            audio_input = gr.Audio(type="filepath", label="Input Audio")
            audio_submit_button = gr.Button("Send Audio")

        # Chat History Display
        state_log_display = gr.Textbox(label="Chat History", lines=10, interactive=False)

        # Connect UI Logic to the Controller
        text_submit_button.click(controller.process_text_input, inputs=text_input, outputs=state_log_display)
        
        # Use the safe handler for audio processing
        audio_submit_button.click(
            lambda x: safe_audio_handler(x, controller), 
            inputs=audio_input, 
            outputs=state_log_display
        )

    # Launch with share=True to address the localhost accessibility issue
    demo.launch(share=True)