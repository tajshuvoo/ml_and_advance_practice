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

load_dotenv()


class ChatState(TypedDict):
    
    messages: Annotated[list[BaseMessage], add_messages]

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct"
)



#tools

search_tools = DuckDuckGoSearchRun(region='en-us')

@tool
def calculator(first_num: float, second_num:float, operation:str )->dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operation: add, sub,mul,div .
    
    Docstring for calculator
    
    :param first_num: Description
    :type first_num: float
    :param second_num: Description
    :type second_num: float
    :param operation: Description
    :type operation: str
    :return: Description
    :rtype: dict
    """
    
    try:
        if operation =="add":
            result = first_num+second_num
        elif operation=="sub":
            result= first_num-second_num
        elif operation=="mul":
            result= first_num*second_num
        elif operation=="div":
            if second_num== 0:
                return {'error':'division by zero is not allowed'}
            result= first_num/second_num
        else:
            return {'error':f"Unsupported operation '{operation}"}
        
        return {'first_num':first_num, 'second_num':second_num , 'operation':operation, 'result':result}
    except Exception as e:
        return {'error': str(e)}
    
@tool
def get_stock_price(symbol: str)-> dict:
    """
    Fetch latest stock price for a given symbol (eg. 'AAPL', 'TSLA')
    using Alpha Vantage with API key in the URL.
    
    Docstring for get_stock_price
    
    :param symbol: Description
    :type symbol: str
    :return: Description
    :rtype: dict
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=EXHDO3AS219UFIEO"
    r = requests.get(url)
    return r.json()


llm = ChatHuggingFace(llm=llm)

tools = [search_tools, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)


def chat_node(state: ChatState):
    
    messages = state['messages']
    
    res = llm_with_tools.invoke(messages)
    
    return {'messages': [res]} 



tool_node = ToolNode(tools)


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)


graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'chat_node')
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge('tools','chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

def retrive_all_thread():
    all_threads = set()
    for ck in checkpointer.list(None):
        all_threads.add(ck.config['configurable']['thread_id'])
        
    return list(all_threads)