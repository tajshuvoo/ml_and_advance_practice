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
        
    res = workflow.invoke({'messages':[HumanMessage(content=user_input)]}, config=config)
    ai_msg = res['messages'][-1].content
    st.session_state['message_history'].append({'role':'ai','content':user_input})
    with st.chat_message('ai'):
        st.text(ai_msg)