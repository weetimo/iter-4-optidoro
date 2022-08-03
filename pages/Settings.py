

import streamlit as st

if 'subject_array' not in st.session_state:
    st.session_state['subject_array'] = subject_array = ["Machine Learning", "HCI and AI", "Service Design Studio", "HASS"]

if 'dev_mode' not in st.session_state:
    st.session_state.dev_mode = False

if 'csv_filepath' not in st.session_state:
    st.session_state['csv_filepath'] = "actual_HCI_data.csv"

st.header("Settings")

with st.form("Add new subject:"):
        new_subject = st.text_input("Add new subject here:")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.subject_array.append(new_subject)
            st.success("New subject added!")

# with st.form("CSV filepath:"):
#     st.caption("If you're getting errors about the CSV filepath, try changing the filepath to a local filepath.")
#     st.caption("Enter your filepath here and click submit.")
#     st.caption("Just filepath only, no quotation marks.")
#     csv_filepath = st.text_input("CSV filepath:")
#     submitted = st.form_submit_button("Submit")
    
#     if submitted:
#         st.session_state.csv_filepath = csv_filepath
#         st.success("CSV filepath updated!")

st.session_state.dev_mode = st.checkbox('dev mode', value=st.session_state.dev_mode)
st.caption("Makes timer run faster for testing purposes.")

if st.session_state.dev_mode == True:
    st.session_state['multiplier'] = 0.001
    #st.write(df)

if st.session_state.dev_mode == False:
    st.session_state['multiplier'] = 1