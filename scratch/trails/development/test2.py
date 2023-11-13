import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Calendly")

clients_data_df=pd.read_csv("F:/Project-11/calendly_reminder/requirements/calendly/cdeclients.csv")
st.write(clients_data_df)

meeting_data_df=pd.read_csv("F:/Project-11/calendly_reminder/requirements/calendly/client_meeting.csv")
st.write(meeting_data_df)

reminders_data_df=pd.read_csv("F:/Project-11/calendly_reminder/requirements/calendly/clients_notmet.csv")
st.write(reminders_data_df)





