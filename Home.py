import streamlit as st
import pandas as pd
import time
from connection.db_conn import sqlalchemy_connect
from connection.db_methods import dbmethods
import datetime as dt



# Defaults
clients_data_file="F:/Project-11/calendly_reminder/requirements/calendly/cdeclients.csv"
wh_token="73bd2696deeaf0acafbb5d4264505d20c70de546"
wh_template_id="PJ5892440"


# Page configuration
st.set_page_config(
    page_title="CMM", 
    page_icon="👨‍✈️", 
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items=None)

# CSS

# Layout
st.title("👨‍✈️ Calendly Meeting Manager")

#connection    
@st.cache_data()
def sq():
    """Database connection and database method collecting from object"""
    return sqlalchemy_connect()

sql=sq()
dbm=dbmethods(connection_link=sql.engine(),connection_object=sql,username='chetan')

tables_dict=sql.read_config()

db_tables=tables_dict["db_tables"]
clients_data_tbl=db_tables["clients_data_table"]
reminders_log_data_tbl=db_tables["reminders_log_data_table"]
meeting_data_tbl=db_tables["meeting_data_table"]


#sessionsstate

#method
def calendly_meeting_data(filepath):
    """Merging of meeting data"""
    clients_data=pd.read_csv(filepath).drop_duplicates('ClientName')
    clients_data['lower_names']=clients_data['ClientName'].str.lower().str.strip().str.replace(" ","")
    meetings_dates_df=dbm.fetch_tables(table_name=meeting_data_tbl,index_col=None).drop_duplicates('name')
    meetings_dates_df['lower_names']=meetings_dates_df['name'].str.lower().str.strip().str.replace(" ","")
    meetings_dates_df=meetings_dates_df.rename(columns={"name":"meetings_data_names"})

    clients_data=pd.merge(clients_data,meetings_dates_df,on="lower_names",how="outer").sort_values(by='meetingtime',ascending=False)
    return clients_data

def reminder_clients_heighlight(s):
    if s > str(dt.datetime.now()):
        return "background-color:blue; color:white; font-size:bold;"
    
current_datetime=dt.datetime.now()

def highlight_greater_than_current_datetime(val):
    return ['background-color: lightgreen' if val > current_datetime else '' for val in meeting_data_df['datetime_column']]

# Apply the styling function to the DataFrame

#table
meeting_data_df=calendly_meeting_data(filepath=clients_data_file)
#styled_meeting_df=meeting_data_df.style.apply(highlight_greater_than_current_datetime, subset=['meetingtime'])
st.dataframe(meeting_data_df)

tbl_col=st.columns((1,1))
pending_meetings_df=meeting_data_df[meeting_data_df['id'].isna() | (meeting_data_df['id'] == '')].reset_index().drop('index',axis=1)
pending_meetings_df.index+=1
with tbl_col[0]:
    st.subheader("🔕 Notmet Clients")
    st.dataframe(pending_meetings_df)

with tbl_col[1]:
    st.subheader("🔔 Reminders Log")
    reminder_log=dbm.fetch_tables(table_name=reminders_log_data_tbl,index_col=None)
    st.dataframe(reminder_log)

with st.expander("📩 Send Reminder",expanded=True):
    st.subheader("🔔 Reminder")
    col=st.columns((1,1))
    first_range=col[0].number_input("✏️ Enter First Index",step=1)
    second_range=col[1].number_input("✏️ Enter Last Index",step=1,max_value=len(pending_meetings_df))
    #name=st.selectbox("name",options=pending_meetings_df['ClientName'])
    but_col=st.columns((10,4,10))
    if but_col[1].button("📩 Send Reminder"):
        df=pending_meetings_df.iloc[first_range:second_range]

        with st.spinner("💬 Sending..."):
            try:
                dbm.send_customers_reminders(df=df,table_name=reminders_log_data_tbl,token=wh_token,template_id=wh_template_id)
                st.success("📩 Send Reminder:Successfull ✔️")
            except Exception as e:
                st.error(e)
                st.error("📩 Send Reminder:Failed ❌")
            time.sleep(2)
            st.experimental_rerun()

