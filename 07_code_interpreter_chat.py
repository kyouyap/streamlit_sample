import traceback
import asyncio
from db_manager import DBManager
from code_interpreter import CodeInterpreter
from datetime import datetime
import streamlit as st

class ChatManager:
    """チャットの管理を担当するクラス。
    DBManagerとCodeInterpreterのインスタンスを持ち、Chatの作成、表示、メッセージの送信等を行う。
    """
    def __init__(self):
        """ChatManagerの初期化を行う。"""
        # データベースとコードインタープリタの初期化
        self.db = DBManager()
        self.ci = CodeInterpreter(self.db)
        # セッションステートの初期化
        if 'current_chat' not in st.session_state:
            st.session_state.current_chat = None
        if 'chats' not in st.session_state:
            st.session_state.chats = self.db.get_chats()
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []

    def run(self):
        """アプリケーションの実行を行う。"""
        # サイドバーでの新規チャット作成ボタンと既存チャットの選択を管理
        with st.sidebar:
            if st.button("New Chat", key="new_chat"):
                chat_title = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                chat_id = self.db.save_chat(chat_title)
                st.session_state.current_chat = self.db.get_chat(chat_id)
                st.session_state.chats = self.db.get_chats()
            st.session_state.current_chat = st.radio("Chat Histories", st.session_state.chats, format_func=lambda x: x[1])

        header_container = st.container()
        chat_container = st.container()
        form_container = st.container()

        if st.session_state.current_chat is None:
            st.caption("Please select a chat history or press 'New Chat' from the sidebar")
        else:
            # チャットの表示
            self.display_chat(header_container, chat_container, form_container)

    def display_chat(self, header_container, chat_container, form_container):
        """指定したチャットの表示を行う。
        
        Args:
            header_container (streamlit.delta_generator.DeltaGenerator): チャットのヘッダー表示に使うコンテナ。
            chat_container (streamlit.delta_generator.DeltaGenerator): チャットのメッセージ表示に使うコンテナ。
            form_container (streamlit.delta_generator.DeltaGenerator): メッセージ送信フォーム表示に使うコンテナ。
        """
        chat_id = st.session_state.current_chat[0]
        chat_title = st.session_state.current_chat[1]
        st.session_state.chat_messages = self.db.get_chat_messages(chat_id)

        with header_container:
            new_chat_title = st.text_input("Chat Title", value=chat_title)
            if st.button("Save Title"):
                self.db.update_chat_title(chat_id, new_chat_title)
                st.session_state.current_chat = self.db.get_chat(chat_id)
                st.session_state.chats = self.db.get_chats()

        with chat_container:
            self.display_chat_messages(chat_container)

        with st.form(key="user_input", clear_on_submit=True):
            self.submit_message(chat_container, chat_id)

    def display_chat_messages(self, chat_container):
        """チャットのメッセージを表示する。
        
        Args:
            chat_container (streamlit.delta_generator.DeltaGenerator): メッセージ表示に使うコンテナ。
        """
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
                    # ダウンロード可能なファイルを表示
                    files = self.db.get_generated_files(chat_message_id)
                    for file in files:
                        data = file[3]
                        file_name = file

    def submit_message(self, chat_container, chat_id):
        """ユーザからのメッセージを受け取り、それに応じて応答を生成して表示する。
        
        Args:
            chat_container (streamlit.delta_generator.DeltaGenerator): メッセージ表示に使うコンテナ。
            chat_id (str): 現在のチャットのID。
        """
        uploaded_files = st.file_uploader("Choose files for analysis:", accept_multiple_files=True)
        text_area = st.text_area("Enter your message:", placeholder="Enter your message", value="")
        if st.form_submit_button("Submit"):
            user_message = text_area
            message_id = self.db.save_message(chat_id, "user", user_message)
            st.session_state.chat_messages.append(self.db.get_chat_message(message_id))
            with chat_container:
                st.chat_message("user").write(user_message)

            try:
                # CodeInterpreterでレスポンスを生成し表示
                response = asyncio.run(self.ci.process(user_message, uploaded_files))
                message_id = self.db.save_message(chat_id, "assistant", response.content)
                st.session_state.chat_messages.append(self.db.get_chat_message(message_id))
                with chat_container:
                    st.chat_message("assistant").write(response.content)
                    for file in response.files:
                        data = file.content
                        file_name = file.name
                        self.db.save_file(message_id, file_name, data)
                        st.download_button(label=f"Download: {file_name}", data=data, file_name=file_name)

            except Exception as e:
                with chat_container:
                    st.write(f"An error occurred: {e.__class__.__name__}: {e}")
                    st.write(traceback.format_exc())

if __name__ == "__main__":
    ChatManager().run()
