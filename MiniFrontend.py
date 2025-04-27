from langchain.schema import HumanMessage
from Workflow import APP
from States import *
import gradio as gr


class RunApp:
    def __init__(self, APP, state):
        self.APP = APP
        self.state: State = state

    def invokeContinuousState(self):
        self.state = self.APP.invoke(self.state)
        return self.state

    def addHumanStateMessage(self, msg):
        print("********************  ADDING MSG  ********************")
        print(msg)
        self.state["messages"].append(HumanMessage(content=msg))
        self.invokeContinuousState()
        return str(self.state)

    def invokeFirstState(self):
        inserted_state: State = {"messages": []}
        self.state = self.APP.invoke(inserted_state)
        print("******* INITIAL STATE: ******")
        print(self.state)
        
        # TODO: actually make pretty log look pretty
        pretty_log = []
        for x in self.state["messages"]:
            pretty_log.append(f"{x.type}: {x.content}")
        
        print("******* PRETTY LOG ******")
        print(pretty_log)
        return pretty_log
    


if __name__ == "__main__":
    
    app = APP
    state: State = {"messages": []}

    runApp = RunApp(APP=app, state=state)
    runApp.invokeFirstState()

    with gr.Blocks() as demo:
        gr.Markdown("# Welcome to L.I.L.I.T.H.")
        gr.Markdown("This is a simple chat interface. Below is the chat history:")

        with gr.Row():
            user_text_input = gr.Textbox(placeholder="say hey!")
            submit_button = gr.Button("Send")

        state_log_display = gr.Textbox(label="Chat History", lines=10, interactive=False)
        submit_button.click(runApp.addHumanStateMessage, inputs=user_text_input, outputs=state_log_display)

        
    demo.launch()
