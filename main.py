from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import streamlit as st

DEFAULT_SYSTEM_PROMPT = """
You are a helpful assistant. Be kind and courteous and helpful.
"""

@st.cache_resource
def get_chat():
    chat = ChatOpenAI(temperature=0, model="gpt-4")
    return chat

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = DEFAULT_SYSTEM_PROMPT

chat = get_chat()

def submit():
    if input := st.session_state.input:
        messages = [
            SystemMessage(content=st.session_state["system_prompt"]),
        ]
        for i, r in st.session_state["chat_history"]:
            messages.append(
                HumanMessage(content=i)
            )
            messages.append(
                AIMessage(content=r)
            )
        messages.append(
            HumanMessage(content=input)
        )            
        result = chat(messages)
        formatted_answer = result.content
        st.session_state.chat_history.append((input, formatted_answer))
        st.session_state.input = ""        

system_prompt = st.text_area("System prompt", key="system_prompt")

for input, response in st.session_state["chat_history"]:
    st.write(f"**You:** \n{input}")
    st.write("\n\n")
    st.write(f"**AI:** \n{response}")
    st.write("\n\n")

    source_texts = ""
    st.write(source_texts)


input = st.text_input("Your input", key="input", on_change=submit)