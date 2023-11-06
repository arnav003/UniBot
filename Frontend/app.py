import streamlit as st
import requests

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = st.secrets["voiceflow_key"]
user_id = st.secrets["user_id"]

st.set_page_config(page_title='UniBot', page_icon='Resources/bot3.png', layout="wide",
                   initial_sidebar_state="collapsed")


def generate_response(user_input):
    url = f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact"

    payload = {"action": {
        "type": "text",
        "payload": f"{user_input}"
    },
        "config": {
            "tts": False,
            "stripSSML": True,
            "stopAll": True,
            "excludeTypes": ["block", "debug", "flow"]
        }
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": api_key
    }

    # Start a conversation
    response = requests.post(
        url=url,
        json=payload,
        headers=headers,
    )
    try:
        output = response.json()
        print(output)
        message = None
        for o in output:
            if o["type"] == 'text':
                message = o["payload"]["message"]
        return message
    except KeyError:
        return "Error occurred. Can't connect to servers."


def chat():
    with st.container():
        if st.session_state.messages == []:
            user_input = f'''Hello!!'''
            st.session_state.messages = [
                {
                    "role": "user",
                    "content": user_input,
                },
            ]
            # response = generate_response(user_input)
            response = '''I am an AI assistant for Manipal University Jaipur.
            Ask me anything!'''
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        for i, message in enumerate(st.session_state.messages[1:]):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])

        user_input = st.chat_input("Enter your query.")

        if user_input is not None and user_input.strip() != "":
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = generate_response(user_input)
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


html = readHTML('Frontend/app.html')
st.markdown(html, unsafe_allow_html=True)

chat()
