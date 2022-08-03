import streamlit as st

st.header("Instructions")
st.write("This is a simple timer that you can use to track your study time across different subjects.")
st.write("The app is laid out as such:")
st.write("1. Home: overview of today's progress")
st.write("2. Dashboard: overview of past study cycles")
st.write("3. Optidoro Timer: smart Pomodoro timer for studying & subject tracking")
#st.write("4. Settings: to add new subjects, fix the CSV error and enable dev mode")
st.write("4. Settings: to add new subjects and enable dev mode")

st.header("Troubleshooting")
# st.write("If you get errors about the CSV filepath, there's a no-code fix in settings.")
st.write("There's a working function to add new subjects in settings.")
st.write("Need the timer to run faster? Enable dev mode in settings.")

st.caption("Optidoro is built by Timothy Wee, with some help from Noah Kong, for HCI and AI, Group 7.")
st.caption("You may contact him at timothy_wee@mymail.sutd.edu.sg for any questions.")