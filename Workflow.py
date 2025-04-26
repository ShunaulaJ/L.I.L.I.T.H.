
from langgraph.graph import StateGraph
from Nodes import *
from States import *

# We'll always print graph, but we don't always invoke the app (for development)
invokeApp = True


workflow = StateGraph(State)
workflow.add_node("intro_tts_node", intro_tts_node)
workflow.add_node("base_llm_node", base_llm_node)

workflow.set_entry_point("intro_tts_node")
workflow.add_edge("intro_tts_node", "base_llm_node")



if __name__ == "__main__":
    # -------- Complie + Graph Layout --------
    APP = workflow.compile()

    # Drawing graph
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