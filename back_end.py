from sqlalchemy import text
from Data_base_con import engine
import base64
import streamlit as st

#Checking the authentication for login
def authenticate_user(username, password):
    try:
        query = text("""
            SELECT user_id, role
            FROM users
            WHERE username = :username AND password = :password

        """)
        
        with engine.connect() as conn:
            result = conn.execute(query, {
                "username" : username,
                "password": password
            }).fetchone() # Fetch one matching record if exists
        return result 
    except Exception as e:
        print("Authentcation Error:",e)
        return None

#Insert a new user query into the queries table.
def insert_query(user_id, email_id, mobile_number, query_heading, query_description, query_datetime):
    try:
        query = text("""
            INSERT INTO queries (
                user_id,
                email_id,
                mobile_number,
                query_heading,
                query_description,
                query_datetime
            )
            VALUES (
                :user_id,
                :email_id,
                :mobile_number,
                :query_heading,
                :query_description,
                :query_datetime
            ) """)

        with engine.connect() as conn:
            conn.execute(query, {
                "user_id": user_id,
                "email_id": email_id,
                "mobile_number": mobile_number,
                "query_heading": query_heading,
                "query_description": query_description,
                "query_datetime": query_datetime
            })
            conn.commit() # Commit transaction to save changes permanently

        return True

    except Exception as e:
        print("Insert Query Error:", e)
        return False

#Retrieve all queries joined with user from the query table  
def get_all_queries():
    try:
        query = text("""
            SELECT 
                q.query_id,
                u.username,
                q.email_id,
                q.mobile_number,
                q.query_heading,
                q.query_description,
                q.status,
                q.query_datetime,
                q.created_at
            FROM queries q
            JOIN users u ON q.user_id = u.user_id
            ORDER BY q.created_at DESC
        """)

        with engine.connect() as conn:
            result = conn.execute(query).fetchall()  # Execute query and fetch all results

        return result

    except Exception as e:
        print("Fetch Queries Error:", e)
        return []

#Create a new user in the users table.  
def create_user(username, password, role):
    try:
        # Check if user already exists
        check_query = text("""
            SELECT 1 FROM users WHERE username = :username
        """)

        insert_query = text("""
            INSERT INTO users (username, password, role)
            VALUES (:username, :password, :role)
        """)

        with engine.connect() as conn:
            exists = conn.execute(check_query, {
                "username": username
            }).fetchone() # Fetch one matching record if exists

            if exists:
                return False  # Username already exists

            conn.execute(insert_query, {
                "username": username,
                "password": password,  
                "role": role
            })
            conn.commit() # Commit the transaction

        return True

    except Exception as e:
        print("Create User Error:", e)
        return False

#Sets a background image for the Streamlit app using CSS  
def set_background(image_path):
    # Read image as binary
    with open(image_path,"rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    # Inject CSS
    st.markdown(
        f"""
         <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True   
    )