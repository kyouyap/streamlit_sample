import traceback
import asyncio
import streamlit as st
from db_manager import DBManager
from code_interpreter import CodeInterpreter
from datetime import datetime

# Initialize database and chat manager
db = DBManager()
ci = CodeInterpreter(db)

# Initialize session states
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = None

if 'chats' not in st.session_state:
    st.session_state.chats = db.get_chats()

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Streamlit UI layout
with st.sidebar:
    if st.button("New Chat", key="new_chat"):
        chat_title = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        chat_id = db.save_chat(chat_title)
        st.session_state.current_chat = db.get_chat(chat_id)
        st.session_state.chats = db.get_chats()
    st.session_state.current_chat = st.radio("Chat Histories", st.session_state.chats, format_func=lambda x: x[1])

header_container = st.container()
chat_container = st.container()
form_container = st.container()

if st.session_state.current_chat is None:
    st.caption("Please select a chat history or press 'New Chat' from the sidebar")
else:
    chat_id = st.session_state.current_chat[0]
    chat_title = st.session_state.current_chat[1]
    st.session_state.chat_messages = db.get_chat_messages(chat_id)

    with header_container:
        new_chat_title = st.text_input("Chat Title", value=chat_title)
        if st.button("Save Title"):
            db.update_chat_title(chat_id, new_chat_title)
            st.session_state.current_chat = db.get_chat(chat_id)
            st.session_state.chats = db.get_chats()

    with chat_container:
        for chat_message in st.session_state.chat_messages:
            chat_message_id = chat_message[0]
            category = chat_message[2]
            content = chat_message[3]
            if category == 'user':
                with st.chat_message("user"):
                    st.write(content)
            else:
                with st.chat_message("assistant"):
                    st.write(content)
                    # Display file download buttons
                    files = db.get_generated_files(chat_message_id)
                    for file in files:
                        data = file[3]
                        file_name = file

    with st.form(key="user_input", clear_on_submit=True):
        uploaded_files = st.file_uploader("Choose files for analysis:", accept_multiple_files=True)
        text_area = st.text_area("Enter your message:", placeholder="Enter your message", value="")
        if st.form_submit_button("Submit"):
            user_message = text_area
            message_id = db.save_message(chat_id, "user", user_message)
            st.session_state.chat_messages.append(db.get_chat_message(message_id))
            with chat_container:
                st.chat_message("user").write(user_message)

            try:
                response = asyncio.run(ci.process(user_message, uploaded_files))
                message_id = db.save_message(chat_id, "assistant", response.content)
                st.session_state.chat_messages.append(db.get_chat_message(message_id))
                with chat_container:
                    st.chat_message("assistant").write(response.content)
                    for file in response.files:
                        data = file.content
                        file_name = file.name
                        db.save_file(message_id, file_name, data)
                        st.download_button(label=f"Download: {file_name}", data=data, file_name=file_name)

            except Exception as e:
                with chat_container:
                    st.write(f"An error occurred: {e.__class__.__name__}: {e}")
                    st.write(traceback.format_exc())