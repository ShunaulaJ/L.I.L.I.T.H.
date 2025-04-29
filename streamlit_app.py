import sys
import os
import streamlit as st
from tempfile import NamedTemporaryFile
from audiorecorder import audiorecorder
from Controllers.HomeMediatingController import HomeMediatingController
from AppCoordinator import AppCoordinator
from ToolKit import Tools
from Workflow import APP
from States import State

# TODO: Log is reseting.. is State reseting? or just the log value
# TODO: Deactivate button for submitting code twice.
# TODO: Currently sends audio thru terminal/local laptop, but web browser 
# TODO: Improve that "submit audio : I'm getting a response", time... that was like 30 seconds

# Add the project root directory to Python's path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



# Initialize session state if not already done
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.full_state_log = ""

def initialize_backend():
    """Initialize the backend components"""
    app = APP
    state = {"messages": []}
    tools = Tools()
    backend = AppCoordinator(APP=app, state=state, tools=tools)
    controller = HomeMediatingController(backend=backend)
    return controller

def process_text_input(text, controller):
    """Process text input and update the session state"""
    if text and text.strip():
        response = controller.process_text_input(text)
        st.session_state.messages.append({"role": "user", "content": text})
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Update the full state log
        st.session_state.full_state_log = response
        return True
    return False

def process_audio_input(audio_file_path, controller):
    """Process audio input and update the session state"""
    try:
        response = controller.process_audio_input(audio_file_path)
        # Extract transcription from response (assuming it's part of the response)
        st.session_state.messages.append({"role": "user", "content": f"[Audio Input]"})
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Update the full state log
        st.session_state.full_state_log = response
        return True
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return False

def main():
    st.set_page_config(page_title="L.I.L.I.T.H.", page_icon="🧠")
    
    # Initialize the controller
    controller = initialize_backend()
    
    # App header
    st.title("🧠 Welcome to L.I.L.I.T.H.")
    st.markdown("Living in loops Improving Through Havoc")
    
    # Create tabs for different views
    chat_tab, state_log_tab = st.tabs(["Chat Interface", "State Logs"])
    
    with chat_tab:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Text input section
        text_col, audio_col = st.columns([3, 1])
        
        with text_col:
            # Text input with send button
            with st.form(key="text_form", clear_on_submit=True):
                user_input = st.text_input("Type your message:", key="text_input")
                submit_button = st.form_submit_button("Send")
                
                if submit_button and user_input:
                    process_text_input(user_input, controller)
                    st.rerun()
        
        with audio_col:
            st.write("Record Audio:")
            
            # Create an audio recorder with start/stop button
            audio_data = audiorecorder("Start Recording", "Stop Recording")
            
            # Check if recording is complete (non-empty audio data)
            if len(audio_data) > 0:
                # Display a player with the recorded audio
                st.audio(audio_data.export().read())
                
                # Create a button to process the recording
                if st.button("Process Recording"):
                    # Save the recorded audio to a temporary file
                    with NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                        audio_data.export(tmpfile.name, format="wav")
                        audio_path = tmpfile.name
                    
                    st.success("Audio recorded! Processing...")
                    
                    # Process the audio file
                    if process_audio_input(audio_path, controller):
                        # Clean up the temporary file
                        try:
                            os.unlink(audio_path)
                        except:
                            pass
                        
                        # Update the UI
                        st.rerun()
            
            # Keep the file uploader as an alternative option
            st.write("Or upload audio file:")
            uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])
            
            if uploaded_file is not None:
                # Save the uploaded audio to a temporary file
                with NamedTemporaryFile(suffix="." + uploaded_file.name.split(".")[-1], delete=False) as tmpfile:
                    tmpfile.write(uploaded_file.getvalue())
                    audio_path = tmpfile.name
                
                st.success("Audio uploaded! Processing...")
                
                # Process the audio file
                if process_audio_input(audio_path, controller):
                    # Clean up the temporary file
                    try:
                        os.unlink(audio_path)
                    except:
                        pass
                    
                    # Update the UI
                    st.rerun()
    
    with state_log_tab:
        # Display full state logs
        st.subheader("Complete State Log")
        st.text_area("", value=st.session_state.full_state_log, height=400, disabled=True)
        
        if st.button("Clear Logs"):
            st.session_state.messages = []
            st.session_state.full_state_log = ""
            st.rerun()

if __name__ == "__main__":
    main()