
from langgraph.graph import StateGraph
from Agents.Nodes import Nodes
from Agents.States import *
from Agents.ToolKit import Tools

# We'll always print graph, but we don't always invoke the app (for development)
invokeApp = True



# TODO: IF WE ARE initizing tools in the frontend file, do I need to do it here?
tools = Tools()
nodes = Nodes(tools=tools)
workflow = StateGraph(State)

workflow.add_node("invoke_base_llm_node", nodes.invoke_base_llm)
workflow.add_node("generate_voice_output_node", nodes.generate_voice_output)

workflow.set_entry_point("invoke_base_llm_node")
workflow.add_edge("invoke_base_llm_node", "generate_voice_output_node")


try: 
    APP = workflow.compile()
except Exception as e:
    print(f"🤬 Error compiling the graph: {e}")
    APP = None

if __name__ == "__main__":
    # -------- Graph Layout --------
    try:
        APP.get_graph().print_ascii()
    except Exception as e:
        # This requires some extra dependencies and is optional
        print(f"Error: {e}")

    print("EDGES IN GRAPH:")
    print(workflow.edges)
    print("-------------------------------------------")

    if invokeApp:
        initial_state: State = {"messages": []}
        final_state = APP.invoke(initial_state)

        print("FINAL STATE:")
        for msg in final_state["messages"]:
            print(f"{msg.type}: {msg.content}")