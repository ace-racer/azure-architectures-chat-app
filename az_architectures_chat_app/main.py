from openai import OpenAI
import streamlit as st
from configs import ANSWER_GENERATION_MODEL, EXPORT_DIR
from utils import export_current_conversation
from chat import get_final_response

st.title("Get answers to your queries on Azure architectures")
st.subheader(f"Conversations will be exported to {EXPORT_DIR} directory.")

# Create a button
export_button = st.button("Export")

if export_button:
    export_current_conversation(st.session_state.messages)

oai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = ANSWER_GENERATION_MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        rag_response = get_final_response(
            oai_client, st.session_state["openai_model"], messages, True
        )
        if not rag_response:
            st.error(
                "Conversation is not related to Azure architectures. Please restart your session.",
                icon="🚨",
            )
        else:
            for response in rag_response:
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
