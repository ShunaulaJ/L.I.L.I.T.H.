from Agents.ToolKit import Tools
from Agents.States import State
from langchain.schema import HumanMessage
from langchain.schema import AIMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# TODO: Improve error handling on the first State Log Input its looking for... 
# TODO: Add logs. 
# TODO: imporve names?

class Nodes:
    def __init__(self, tools: Tools):
        self.tools = tools
    
    # def process_user_input(self, state: State) -> State:
    #     msg = state["messages"][-1]
    #     if msg.metadata.get("input_type") == "text":
    #         print("********************  PROCESSING TEXT INPUT  ********************")
    #         return state["messages"].append(HumanMessage(content=msg.content))
    #     elif msg.metadata.get("input_type") == "audio":
    #         print("********************  PROCESSING AUDIO FILE  ********************")
    #         return state["messages"].append(HumanMessage(content=self.tools.get_tts(file=audio)))
    #         # return {"messages": [HumanMessage(tools.get_tts(file=audio))]}
    #     else:
    #         print("********************  ERROR: NO INPUT  ********************")
    #         return state
        
    def invoke_base_llm(self, state: State) -> State:
        llm = ChatOpenAI(api_key=self.tools.api_key, model="gpt-4.1-mini")
        try:
            response = llm.invoke([state["messages"][-1]])
            state["messages"].append(AIMessage(content=response.content))
        except Exception as e:
            print(f"🤬 Error in LLM invocation: {e}")
        return state
        
    def generate_voice_output(self, state: State) -> State:
        try:
            getAudioData = self.tools.get_elev_voice(text=(state["messages"][-1].content))
            # TODO: Make sure to add the proper value
            log = (f"SPOKEN: {getAudioData}")
            print(log)
            state["messages"].append(AIMessage(content=log))
        except Exception as e:
            print(f"🤬 Error in ELEVEN Voice invocation: {e}")

        return state
    

