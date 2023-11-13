import requests
import pandas as pd
from pathlib import Path
import json
import pdb
import streamlit as st
#Loop thro 4 months and get all the events

url="https://api.calendly.com/scheduled_events?organization=https://api.calendly.com/organizations/CHHCQYYBK6CI5GMA"
#headers = {'content-type': 'application/soap+xml'}
headers1 = {'content-type': 'application/json','Authorization' : 'Bearer eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjk1NjI2NDE3LCJqdGkiOiJmNzEzZTQ5Ny03ZWJkLTQ0OTYtOTc3Ni03ZTdiMjk3NjlkMzkiLCJ1c2VyX3V1aWQiOiJHRUhIWFkyQ09QSklYWlI2In0.JVBCRR2z2kO6VbdULl9AOhmOR3K7hHasqWXwcOTbvaHr3HEEABGgQhe1HXvPjsLQD1oNkkbUwooliprhKe-5rw'}

for i in range(9,12):
    if i == 9:
        is1 = "0" + "9"
    else:
        is1 = str(i)
    is2 = i + 1
    minstarttime = "2023-" + str(is1) + "-01 T12:30:00.000000Z"
    maxstarttime = "2023-" + str(is2) + "-01 T12:30:00.000000Z"
    print(minstarttime)
    print(maxstarttime)
    #params = {'count':'100','min_start_time':'2023-09-01T12:30:00.000000Z','max_start_time':'2023-10-01T12:30:00.000000Z'}
    params = {'count':'100','min_start_time': minstarttime,'max_start_time': maxstarttime}

    response = requests.get(url=url,params=params,headers=headers1)

    #print(calendly.echo())
    print(params)
    print(response.text)

    #with open('events.json', 'w', encoding='utf-8') as f:
    #    json.dump(response.text, f, ensure_ascii=False, indent=4)

    #with open("events.json") as jsonFile:
    data = json.loads(response.text)
    # create dataframe
    df = pd.json_normalize(data)
    jsonData = pd.json_normalize(data["collection"])
    if i == 9:
        st.dataframe(jsonData,use_container_width=True)
        #jsonData.to_csv('events.csv',index=False, encoding='utf-8')
    else:
        st.dataframe(jsonData,use_container_width=True)
        #jsonData.to_csv('events.csv',header=False,mode='a',index=False, encoding='utf-8')