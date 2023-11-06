import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

PAGE_INDEX = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = st.secrets["voiceflow_key"]
user_id = st.secrets["user_id"]

st.set_page_config(page_title='UniBot', page_icon='Resources/bot_full_square_transparent.png', layout="wide",
                   initial_sidebar_state="collapsed")

with st.sidebar:
    pages = ["Chat", "Admin"]
    pages_id = ["app", "admin"]
    pages_icon = ["chat-left", "person-check"]
    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=pages_icon,
        default_index=PAGE_INDEX
    )
    if pages.index(selected) != PAGE_INDEX:
        if selected == 'Chat':
            switch_page("app")
        if selected == 'Admin':
            switch_page("admin")


def generate_response(user_id, request):
    with st.spinner("Thinking..."):
        url = f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact"

        # payload = {"action": {
        #     "type": "text",
        #     "payload": f"{user_input}"
        # },
        #     "config": {
        #         "tts": False,
        #         "stripSSML": True,
        #         "stopAll": True,
        #         "excludeTypes": ["block", "debug", "flow"]
        #     }
        # }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": api_key
        }

        # Start a conversation
        response = requests.post(
            url=url,
            json={'request': request},
            headers=headers,
        )
        try:
            output = response.json()
            message = ""
            for trace in output:
                if trace["type"] == 'text' or trace["type"] == 'speak':
                    message = message + trace["payload"]["message"]
                elif trace['type'] == 'end':
                    return None
            return message
        except KeyError:
            return "Error occurred. Can't connect to servers."


def chat():
    with st.container():
        if st.session_state.messages == []:
            response = generate_response(user_id, {'type': 'launch'})
            if response == None:
                response = '''I am an AI assistant for Manipal University Jaipur.
                Ask me anything!'''
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                with st.chat_message(name="user", avatar="./Resources/user.jpeg"):
                    st.write(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message(name="assistant", avatar="./Resources/bot_head_square.png"):
                    st.write(message["content"])

        user_input = st.chat_input("Enter your query.")

        if user_input is not None and user_input.strip() != "":
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message(name="user", avatar="./Resources/user.jpeg"):
                st.write(user_input)
            response = generate_response(user_id, {'type': 'text', 'payload': user_input})
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()


def readHTML(htmlFile):
    file = open(htmlFile, 'r')
    lines = file.readlines()
    file.close()
    html = ""
    for line in lines:
        html += line
    return html


st.markdown(readHTML('Frontend/app.html'), unsafe_allow_html=True)
chat()
