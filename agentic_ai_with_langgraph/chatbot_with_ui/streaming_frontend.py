import streamlit as st 
from backend import workflow
from langchain_core.messages import HumanMessage

config = {'configurable':{ 'thread_id': 'thread-1'}}
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

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
                config = {'configurable':{ 'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
        )
        
        st.session_state['message_history'].append({'role':'ai','content':ai_msg})