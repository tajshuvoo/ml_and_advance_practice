import streamlit as st 
from backend import workflow, retrive_all_thread
from langchain_core.messages import HumanMessage
import uuid


#utility function
def gen_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = gen_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id']) 
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)


def load_conv(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


#session setup

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = gen_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = retrive_all_thread()

add_thread(st.session_state['thread_id'])
config = {'configurable':{ 'thread_id': st.session_state['thread_id']}}



#sidebar ui 
st.sidebar.title('Llama Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(thread_id)):
        
        st.session_state['thread_id'] = thread_id
        messages = load_conv(thread_id)
        
        temp_msg=[]
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role ='user'
            else:
                role='ai'
            temp_msg.append({'role':role , 'content': msg.content})
        st.session_state['message_history'] = temp_msg
        



#main ui
for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])
        
user_input = st.chat_input('Type Here...') 

if user_input:
    
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
   
    # st.session_state['message_history'].append({'role':'ai','content':user_input})
    with st.chat_message('ai'):
        ai_msg = st.write_stream(
         
            msg_chunk.content for msg_chunk , meta_data in  workflow.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config = {'configurable':{ 'thread_id': st.session_state['thread_id']},
                          'metadata':{
                              'thread_id': st.session_state['thread_id']
                          },
                          'run_name':'chat_turn'
                          },
                stream_mode='messages'
            )
        )
        
        st.session_state['message_history'].append({'role':'ai','content':ai_msg})