import streamlit as st

import time
import pandas as pd
from datetime import datetime
# import numpy as np

from gspread_pandas import Spread,Client
from google.oauth2 import service_account

import random

if 'user' not in st.session_state:
    st.session_state['user'] = random.random()

# Disable certificate verification
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "HCI and AI"
spread = Spread(spreadsheetname,client = client)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Spreadsheet (database) Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

#get a list of all keys in st.session_state


# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Timestamp','User', 'session_type', 'Effort', 'Fatigue', 'minutes_today',
    'cancel_clicked', 'break_minutes', 'extend_counter', 'countdown_time', 'form_on',
    'extend_clicked', 'cycle_counter', 'extend', 'time_minutes', 'begin_clicked',
    'daily_focus_score', 'daily_effort_score', 'dev_mode'
    
    
    ]
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    

from gsheetsdb import connect
gsheet_url = "https://docs.google.com/spreadsheets/d/19xhszrZtww1Z-x3WeOSm2zW9D8TqqIAHWNzH8En9IY4/edit?usp=sharing"

@st.cache()
def begin_connection():
    global conn
    conn = connect()
    return

begin_connection()

if 'disable_begin' not in st.session_state:
    st.session_state['disable_begin'] = False

if 'run_finished' not in st.session_state:
    st.session_state['run_finished'] = False

if 'begin_clicked' not in st.session_state:
    st.session_state['begin_clicked'] = False

if 'extend' not in st.session_state:
    st.session_state['extend'] = False

if 'session_type' not in st.session_state:
    st.session_state['session_type'] = 'Modified Pomodoro'

# st.write(st.session_state)

def begin_callback():
    # st.session_state['break_minutes'] += 5
    st.session_state['countdown_time'] = time_minutes * 60
    st.session_state.run_finished = False
    st.session_state.cancel_clicked = False
    st.session_state.begin_clicked = True 
    st.session_state['minutes_today'] += 25
    st.session_state['extend_counter'] = 0



if 'cancel_clicked' not in st.session_state:
    st.session_state['cancel_clicked'] = False

def cancel_callback():
    #st.session_state['break_minutes'] -= 5 + st.session_state['extend_counter'] * 5
    st.session_state.run_finished = True
    st.session_state.begin_clicked = False
    st.session_state.cancel_clicked = True 
    #st.session_state['extend_counter'] = 0
    #st.session_state['disable_begin'] = False
    st.session_state['minutes_today'] -= (25 * st.session_state['extend_counter'] + 25)


if 'extend_clicked' not in st.session_state:
    st.session_state['extend_clicked'] = False

def extend_callback():
    st.session_state['countdown_time'] += 1500
    st.session_state.run_finished = False
    st.session_state.cancel_clicked = False
    st.session_state.begin_clicked = True 
    st.session_state['extend'] = True
    st.session_state['extend_counter'] += 1
    st.session_state['minutes_today'] += 25 #check this
    #combined_count_down(st.session_state['countdown_time'])

if 'countdown_time' not in st.session_state:
    st.session_state['countdown_time'] = 0

if 'break_minutes' not in st.session_state: 
    st.session_state['break_minutes'] = 2700

if 'time_minutes' not in st.session_state:
    st.session_state['time_minutes'] = 0

if 'minutes_today' not in st.session_state:
    st.session_state['minutes_today'] = 0

if 'form_on' not in st.session_state:
    st.session_state.form_on = False

if 'dev_mode' not in st.session_state:
    st.session_state.dev_mode = True

if 'cycle_counter' not in st.session_state: 
    st.session_state['cycle_counter'] = 0

if 'multiplier' not in st.session_state:
    st.session_state['multiplier'] = 1 #change this to 1 in deployment

if 'daily_focus_score' not in st.session_state:
    st.session_state['daily_focus_score'] = 0

if 'daily_effort_score' not in st.session_state:
    st.session_state['daily_effort_score'] = 0

if 'extend_counter' not in st.session_state:
    st.session_state['extend_counter'] = 0

def combined_count_down(ts):

    with st.empty():
        
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(float(st.session_state['multiplier']))
            ts -= 1
            st.session_state['countdown_time'] -= 1
        
        st.session_state.run_finished = True

        st.success("Work cycle over! Time for a break!")

        #begin break counter
        
        # st.session_state['minutes_today'] += 25
        st.session_state['cycle_counter'] += 1
        st.session_state.form_on = True
        st.experimental_rerun()
    return

st.title("Optidoro Timer")

if st.session_state['minutes_today'] <= 100:
    progress_bar = st.session_state['minutes_today']
else:
    progress_bar = 100

st.progress(progress_bar)
st.caption("Learning Faster & Greater")
#st.write(st.session_state)

#st.line_chart(df)
time_minutes = 25
global break_time_minutes
break_time_minutes = 5

# st.write(st.session_state)
mins, secs = divmod(st.session_state['break_minutes'], 60)
time_now = '{:02d}:{:02d}'.format(mins, secs)

break_mins, break_secs = divmod(st.session_state['break_minutes'], 60)
break_time_now = '{:02d}:{:02d}'.format(break_mins, break_secs)
st.metric("Remaining break time", break_time_now)

if (st.button("Begin work cycle", on_click=begin_callback, disabled=st.session_state['disable_begin']) or st.session_state['extend']): #or st.session_state['autopilot_work']: #how to hide begin button when timer is running?
    if st.session_state['countdown_time'] != 0:
        st.write("Work cycle in progress")
    
    if not st.session_state.run_finished:
        
        if st.button("Extend your current cycle", help="Extends current work cycle by 25 minutes.", on_click=extend_callback):
            pass

        if st.button("End current cycle", help="By clicking this button, you will end your current work cycle. Time spent on this cycle will not be counted.", on_click=cancel_callback): #fix 
            pass

    if not st.session_state.cancel_clicked:
        st.session_state['extend'] = False
        #st.session_state['disable_begin'] = True
        combined_count_down(st.session_state['countdown_time'])
        

if st.session_state.cancel_clicked:
    st.session_state.cancel_clicked = False
    st.experimental_rerun()

if not st.session_state['disable_begin']:
    st.session_state['disable_begin'] = False

#st.write(df)

if st.session_state.form_on: #triggers when timer is up

    with st.form("How was the session?"):
        effort_score = st.slider("Effort score: ", min_value=1, max_value=10, value=5)
        focus_score = st.slider("Fatigue score: ", min_value=1, max_value=10, value=5)
        st.write("Click the begin button to start your next session.")
        submitted = st.form_submit_button("Save and start break", help='This will start counting down your remaining break time.') #submit

        if submitted:
        #import CSV as a dataframe
            st.session_state['daily_focus_score'] += focus_score
            st.session_state['daily_effort_score'] += effort_score
            st.session_state.form_on = False
            now = datetime.now()
            opt = {'Timestamp': now, 'User': st.session_state['user'], 'session_type': st.session_state['session_type'], 
                    'Effort': effort_score, 'Fatigue': focus_score, 'minutes_today': st.session_state['minutes_today'], 
                    'cancel_clicked': st.session_state['cancel_clicked'], 'break_minutes': st.session_state['break_minutes'],
                    'extend_counter': st.session_state['extend_counter'], 'countdown_time': st.session_state['countdown_time'],
                    'form_on': st.session_state['form_on'], 'extend_clicked': st.session_state['extend_clicked'],'cycle_counter': st.session_state['cycle_counter'],
                    'extend': st.session_state['extend'], 'time_minutes': st.session_state['time_minutes'], 
                    'begin_clicked': st.session_state['begin_clicked'], 'daily_focus_score': st.session_state['daily_focus_score'], 'daily_effort_score': st.session_state['daily_effort_score'],
                    'dev_mode': st.session_state['dev_mode']
                    }
            opt_df = pd.DataFrame(opt, index=[0])
            df = load_the_spreadsheet('data')
            new_df = df.append(opt_df, ignore_index=True)
            update_the_spreadsheet('data', new_df)

            st.session_state.form_on = False
            st.success('Your effort score and focus score have been recorded. Please wait while we start your break.')
            #st.write(df)
            
            time.sleep(2)
            # st.experimental_rerun()

            st.header("Break time!")
            # ts = break_time_minutes * 60
            ts = st.session_state['break_minutes']
            
            with st.empty():
                while ts:
                    mins, secs = divmod(ts, 60)
                    time_now = '{:02d}:{:02d}'.format(mins, secs)
                    st.header(f"{time_now}")
                    time.sleep(float(st.session_state['multiplier']))
                    #st.session_state['']
                    ts -= 1
                    st.session_state['break_minutes'] -= 1
            
            st.success("Break cycle over! ")
            time.sleep(2)
            st.experimental_rerun()

#create a dataframe called graph_df from df, with only the timestamp, subject, and minutes_today columns

st.metric("Minutes today", st.session_state['minutes_today'])

dev_mode = st.checkbox('dev mode', value=st.session_state.dev_mode)
st.caption("Makes timer run faster for testing purposes.")

if dev_mode == True:
    st.session_state.dev_mode == True
    st.session_state['multiplier'] = 0.005

if dev_mode == False:
    st.session_state['multiplier'] = 1
    st.session_state.dev_mode == False

if st.session_state['minutes_today'] >= 100:
    st.write("You have completed the study! Congratulations! Submit your scores, and enjoy the remainder of your break!")
    link = "[Proceed to post-test survey] (https://forms.gle/dY5VJVyzKEVWMV1w9)"
    st.markdown(link, unsafe_allow_html=True)