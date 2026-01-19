import streamlit as st
from back_end import create_user,set_background

st.set_page_config(page_title="Create User")
set_background("D:/Logesh/login_page_3.jfif")
st.title("Create New User")

# Form for creating a new user credential
with st.form("Create_User_Form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    role = st.selectbox("Role", ["client", "support"])
    create_btn = st.form_submit_button("Create User")

if create_btn:
    if not username or not password or not confirm_password:
        st.error("All fields are mandatory")
    elif password != confirm_password:
        st.error("Password do not match")
    else:
        success = create_user(username,password, role)

        if success:
            st.success("User Credential Created Successfully")
        else:
            st.error("User Already Exists")