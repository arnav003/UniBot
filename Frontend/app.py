import streamlit as st

st.set_page_config(page_title='UniBot', page_icon='Resources/bot2.png', layout="wide",
                   initial_sidebar_state="collapsed")

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
