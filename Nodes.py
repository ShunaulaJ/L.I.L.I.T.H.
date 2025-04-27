from ToolKit import Tools
from States import State
from langchain.schema import HumanMessage
from langchain.schema import AIMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# TODO: Improve error handling on the first State Log Input its looking for

def intro_tts_node(state: State) -> State:
    tools = Tools()
    getText = tools.get_tts()
    print(getText)
    state["messages"].append(HumanMessage(content=getText))

    return state

def base_llm_node(state: State) -> State:
    tools = Tools()
    llm = ChatOpenAI(api_key=tools.api_key, model="gpt-4.1-mini")
    messages = state["messages"]
    try:
        response = llm.invoke([messages[-1]])
        state["messages"].append(AIMessage(content=response.content))
    except Exception as e:
        print(f"🤬 Error in LLM invocation: {e}")

        
    
    return state

# TODO: Honestly unsure if this node needs to continue state updates. It's just a txt-speech node, maybe as a log..
def outro_tts_node(state: State) -> State:
    tools = Tools()
    try:
        getAudioData = tools.get_elev_voice(text=(state["messages"][-1].content))
        # TODO: Make sure to add the proper value
        log = (f"SPOKEN: {getAudioData}")
        print(log)
        state["messages"].append(AIMessage(content=log))
    except Exception as e:
        print(f"🤬 Error in ELEVEN Voice invocation: {e}")

    return state