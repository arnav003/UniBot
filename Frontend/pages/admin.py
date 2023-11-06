import base64

import pandas as pd
import streamlit as st

if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False
if 'book_df' not in st.session_state:
    st.session_state['book_df'] = None
if 'faculty_df' not in st.session_state:
    st.session_state['faculty_df'] = None
if 'event_df' not in st.session_state:
    st.session_state['event_df'] = None


def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


if st.session_state['admin_logged_in'] == False:
    st.markdown('### Welcome to Admin Portal')
    ad_user = st.text_input("Username")
    ad_password = st.text_input("Password", type='password')
    if st.button('Login'):
        if ad_user == st.secrets["admin_id"] and ad_password == st.secrets["admin_pass"]:
            st.session_state['admin_logged_in'] = True
            st.rerun()
        else:
            st.error("Wrong ID or Password.")
else:
    # st.success("Welcome Admin")

    st.markdown('### Admin Portal')

    with st.expander(label="Add new book", expanded=False):
        name = st.text_input("Book Name")
        author = st.text_input("Author")
        publisher = st.text_input("Publisher")
        subject = st.text_input("Subject")

        if st.button('Add listing', key="book"):
            if st.session_state.book_df is None:
                st.session_state.book_df = pd.DataFrame(data={"Book Name": [name,], "Author": [author,], "Publisher": [publisher,], "Subject": [subject,]})
            else:
                st.session_state.book_df.loc[len(st.session_state.book_df)] = [name, author, publisher, subject]

        if st.session_state.book_df is not None:
            st.markdown(get_table_download_link(st.session_state.book_df, "new_books.txt", "Download Data"),
                        unsafe_allow_html=True)

    with st.expander(label="Add new faculty", expanded=False):
        name = st.text_input("Name")
        department = st.text_input("Department")
        post = st.text_input("Post")
        email = st.text_input("Email")
        phone = st.text_input("Phone")

        if st.button('Add listing', key="faculty"):
            if st.session_state.book_df is None:
                st.session_state.book_df = pd.DataFrame(data={"Name": [name,], "Department": [department,], "Post": [post,], "Email": [email,], "Phone": [phone,]})
            else:
                st.session_state.book_df.loc[len(st.session_state.book_df)] = [name, department, post, email, subject]

        if st.session_state.book_df is not None:
            st.markdown(get_table_download_link(st.session_state.book_df, "new_faculty.csv", "Download Data"),
                        unsafe_allow_html=True)

    with st.expander(label="Add new event", expanded=False):
        club = st.text_input("Club Name")
        event = st.text_input("Event Name")
        desc = st.text_input("Event Description")
        date = st.text_input("Date")
        venue = st.text_input("Venue")

        if st.button('Add event', key="event"):
            if st.session_state.book_df is None:
                st.session_state.book_df = pd.DataFrame(data={"Club Name": [club,], "Event Name": [event,], "Event Description": [desc,], "Date": [date,], "Venue": [venue,]})
            else:
                st.session_state.book_df.loc[len(st.session_state.book_df)] = [club, event, desc, date, venue]

        if st.session_state.book_df is not None:
            st.markdown(get_table_download_link(st.session_state.book_df, "new_event.csv", "Download Data"),
                        unsafe_allow_html=True)

    if st.button("Log out"):
        st.session_state['admin_logged_in'] = False
        st.rerun()