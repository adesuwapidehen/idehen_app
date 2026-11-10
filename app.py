import os
from datetime import datetime

import boto3
import streamlit as st

TABLE_NAME = os.environ.get("TABLE_NAME", "idehen_table")
REGION = os.environ.get("AWS_REGION", "us-east-1")

table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE_NAME)

st.title("Welcome to Elohor Idehen's webpage")

FIELDS = ["firstname", "lastname", "dob"]
for f in FIELDS:
    st.session_state.setdefault(f, "")


def start_over():
    for f in FIELDS:
        st.session_state[f] = ""


st.text_input("Firstname", key="firstname")
st.text_input("Lastname", key="lastname")
st.text_input("Date of Birth (mm/dd/yyyy)", key="dob")

col1, col2 = st.columns(2)
submit = col1.button("Submit")
col2.button("Start Over", on_click=start_over)

if submit:
    first = st.session_state.firstname.strip()
    last = st.session_state.lastname.strip()
    dob = st.session_state.dob.strip()
    if not (first and last and dob):
        st.error("Please fill in all three fields.")
    else:
        try:
            datetime.strptime(dob, "%m/%d/%Y")
        except ValueError:
            st.error("Date of birth must be in mm/dd/yyyy format.")
        else:
            try:
                table.put_item(Item={"lastname": last, "firstname": first, "dob": dob})
                st.success(f"Saved {first} {last} ({dob}) to {TABLE_NAME}.")
            except Exception as e:
                st.error(f"Could not save to DynamoDB: {e}")
