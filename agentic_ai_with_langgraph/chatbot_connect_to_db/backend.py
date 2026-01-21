from langgraph.graph import StateGraph, START, END
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

load_dotenv()


class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage], add_messages]

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0
)

model = ChatHuggingFace(llm=llm)

def chat_node(state: ChatState):
    
    messages = state['messages']
    
    res = model.invoke(messages)
    
    return {'messages': [res]} 


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

workflow = graph.compile(checkpointer=checkpointer)

def retrive_all_thread():
    all_threads = set()
    for ck in checkpointer.list(None):
        all_threads.add(ck.config['configurable']['thread_id'])
        
    return list(all_threads)