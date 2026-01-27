from langgraph.graph import StateGraph, START, END
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage,BaseMessage
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3
import requests
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()


class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage], add_messages]

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct"
)


client= MultiServerMCPClient(
    {
        "expense":{
            "transport":"stdio",
            "command":"python3",
            "args":["/Users/tajbirhasanshuvo/academicfiles/expense-tracker-mcp-server/main.py"]
        }
    }
)



llm = ChatHuggingFace(llm=llm)


async def build_graph():
    
    tools = await client.get_tools()
    
    llm_with_tools = llm.bind_tools(tools)
    
    async def chat_node(state: ChatState):
    
        messages = state['messages']
        
        res =await llm_with_tools.ainvoke(messages)
        
        return {'messages': [res]} 



    tool_node = ToolNode(tools)


    graph = StateGraph(ChatState)

    graph.add_node('chat_node', chat_node)
    graph.add_node('tools', tool_node)

    graph.add_edge(START, 'chat_node')
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge('tools','chat_node')

    chatbot = graph.compile()
    
    return chatbot

async def main():

    chatbot = await build_graph()

    # running the graph
    result = await chatbot.ainvoke({"messages": [HumanMessage(content="summury of  expenses jan 2026 full month")]})

    print(result['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())