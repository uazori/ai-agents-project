 #Implement simple agent that writes tests based only on source code context 

import os
from typing import Literal
from typing import Annotated
from dotenv import load_dotenv
from dotenv import find_dotenv
from langchain_openai import ChatOpenAI
from resumeLoader import get_job, get_resume
from vector import retriver
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph,START,END,MessagesState,add_messages
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.globals import set_debug,set_verbose
from langchain_core.tools import tool
from fileTools import read_file_as_text
from IPython.display import Image, display

print("Loading environment variables...")
load_dotenv(find_dotenv(),verbose=True)
print("Environment variables loaded.")
config = {"configurable": {"thread_id": "1"}}

set_debug(True)  # Enable debug mode for LangGraph
#set_verbose(True)  # Enable verbose output for LangGraph

#Create agent that is going to write unit tests for the given project 

class State(TypedDict):
    messages: Annotated[list, add_messages(format='langchain-openai')]

@tool
def readCodeTool() -> str:
    """Get code file."""
    file_path = "/Users/vadymo/code/chessrating/chess-rating-server/src/main/java/com/millhouse/chessrating/service/GameServiceImp.java"
    fileCode = read_file_as_text(file_path)
    print("fileCode lenth - ", len(fileCode))
    return fileCode


#print("fileCode - ", readCodeTool)
#tools = [get_job, get_resume]
tools = [readCodeTool]
# Define the config
llm = ChatOpenAI(model="gpt-4o", temperature=0.0,api_key=os.getenv("OPENAI_API_KEY"))
#.bind_tools(tools)

def expert_agent(state: State):
    print("-----------Expert agent invoked with state:", state)
    system_message = """You are an expert agent that writes tests for code from the tool"""
    messages = state["messages"]
    response = llm.invoke([system_message]+messages)
    print("------------Response from LLM:", response)
    return {"messages": [response]}

# MessagesState will keep on inserting messages while passing every Node
def node1(state: State):
    print("Node-1 invoked with state:", state)
    input1 = state['messages'][0].content # Use list index to access the content
    response = str(input1) + ", From Node-1: Hello, Human"
    return {"messages": [response]}

def chatbot_node(state: State) -> list:
    return {"messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Here's an image:",
                    "cache_control": {"type": "ephemeral"},
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": "1234",
                    },
                },
            ]
        },
    ]}

tool_node = ToolNode(tools)

def should_continue(state: State) -> Literal["tools",END]:
   print("--------------Should continue invoked with state:", state)
   messages = state["messages"]
   print("---------------messages - ", messages)
   last_message = messages[-1]
   return tools #if isinstance(last_message, HumanMessage) else END
  # if last_message.tool_calls:
   #     return "tools"
   
   return END
# Define a new graph
checkpointer = InMemorySaver()
graphBuilder = StateGraph(State)

# builder.add_node("chatbot", chatbot_node)
graphBuilder.add_node("expert", expert_agent)
# builder.add_node("node1", node1)
graphBuilder.add_node("tools", tool_node)


graphBuilder.add_edge(START, "expert")
#builder.add_conditional_edges("expert",should_continue)
graphBuilder.add_edge("expert", "tools")
graphBuilder.add_edge("tools", END)
#builder.add_edge("expert", "node1")

# builder.add_node("node1", node1)
# builder.set_entry_point("chatbot")
# builder.set_finish_point("chatbot")
#graph = builder.compile()
# responce = graph.invoke({"messages": []})

#checkpointer = InMemorySaver()

app = graphBuilder.compile(checkpointer=checkpointer)
graphDraw2 = app.get_graph().draw_ascii()
print("------Graph ASCII representation:\n", graphDraw2)
graphDraw = app.get_graph().draw_mermaid_png()
try:
    #print("-----------Displaying the graph image.",app.get_graph())
    #print("Graph png",graphDraw)
    display(Image(graphDraw))
except Exception:
    print("-----------Failed to display the graph image. This might be due to missing dependencies for rendering images.")
    print("--------Exception: ",Exception)
    # This requires some extra dependencies and is optional
    pass

while True:
    user_input = input("Enter your message (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Exiting the application.")
        break
    try:        
        initial_state: State = {
    "messages": [user_input],
    "sender": "user"
}
        #messages=[HumanMessage(content=user_input)]
        responce = app.invoke(initial_state)
        print("Response from the agent:", responce["messages"][-1].content)
        print( list(app.get_state_history(config)))

    except Exception as e:
        print(f"An error occurred: {e}")
        break