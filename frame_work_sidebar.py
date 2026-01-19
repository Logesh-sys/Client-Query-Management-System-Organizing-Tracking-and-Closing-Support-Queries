import streamlit as st
from datetime import datetime
import pandas as pd
from back_end import authenticate_user,insert_query,get_all_queries,set_background

current_dt = datetime.now()

st.set_page_config(page_title="Query Portal", layout="centered")
set_background("D:/Logesh/login_page_3.jfif")

st.title("Query Portal")

# ---------- SESSION STATE ----------
if "role" not in st.session_state:
    st.session_state.role = None   # None | "client" | "support"

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("Navigation")

    # NOT LOGGED IN
    if st.session_state.role is None:
        st.info("Please login")

    # CLIENT NAVIGATION
    elif st.session_state.role == "client":
        st.success("Client Portal")

        if st.button("Submit Query"):
            st.session_state.page = "home"
            st.rerun()

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # SUPPORT NAVIGATION
    elif st.session_state.role == "support":
        st.success("Support Portal")

        if st.button("Dashboard"):
            st.session_state.page = "home"
            st.rerun()

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

# ---------- MAIN CONTENT ----------
# CLIENT FLOW
if st.session_state.role is None:
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("User Name")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    
    #  login form submission
    if submit:
        if not username or not password:
            st.error("All fields are mandatory")
        else:
            user = authenticate_user(username, password) # Check credentials

            if user:
                st.session_state.user_id = user.user_id
                st.session_state.role = user.role
                st.session_state.page = "home"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

# ---------- CLIENT PAGES ----------
elif st.session_state.role == "client":

    if st.session_state.page == "home":
        st.subheader("Query Submission Page")

        # Client query submission form
        with st.form("query_form"):
            email_id = st.text_input("Email ID *")
            mobile_number = st.text_input("Mobile Number *")
            query_heading = st.text_input("Query Heading *")
            query_description = st.text_area("Query Description *")
            date_time = st.datetime_input(
                "Select Date & Time",
                min_value=current_dt,
                max_value=current_dt,
                value=current_dt
            )
            agree = st.checkbox("I agree all required fields are filled *")
            submit_query = st.form_submit_button("Submit Query")

        if submit_query:
            if not email_id or not mobile_number or not query_heading or not query_description:
                st.error("All fields are mandatory")
            elif not agree:
                st.error("You must agree before submitting")
            else:
                success = insert_query(
                    st.session_state.user_id,
                    email_id,
                    mobile_number,
                    query_heading,
                    query_description,
                    date_time
                )

                if success:
                    st.success("Query Submitted Successfully!")
                else:
                    st.error("Failed to submit query. please try again")

# ---------- SUPPORT TEAM PAGES ----------
elif st.session_state.role == "support":

    if st.session_state.page == "home":
        st.subheader("Support Team Dashboard")
        
        # Fetch all queries from database
        queries = get_all_queries()

        if not queries:
            st.info("No queries available")
        else:
            df = pd.DataFrame(queries, columns=[
                "Query ID",
                "User Name",
                "Email ID",
                "Mobile Number",
                "Query Heading",
                "Query Description",
                "Status",
                "Query DateTime",
                "Created At"
            ])
            df.insert(0, 'S.No', range(1, len(df) + 1)) # Add serial number as first column

            st.dataframe(df,width='content') # Display DataFrame in Streamlit
