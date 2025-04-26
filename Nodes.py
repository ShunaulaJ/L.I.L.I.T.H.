from ToolKit import Tools
from States import State
from langchain.schema import HumanMessage
from langchain.schema import AIMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI

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
    response = llm.invoke([messages[-1]])
    state["messages"].append(AIMessage(content=response.content))
    
    return state