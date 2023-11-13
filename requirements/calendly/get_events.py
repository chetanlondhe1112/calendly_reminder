import requests
import pandas as pd
from pathlib import Path
import json
import pdb
#from calendly import Calendly

#api_key = 'eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjk1NjI2NDE3LCJqdGkiOiJmNzEzZTQ5Ny03ZWJkLTQ0OTYtOTc3Ni03ZTdiMjk3NjlkMzkiLCJ1c2VyX3V1aWQiOiJHRUhIWFkyQ09QSklYWlI2In0.JVBCRR2z2kO6VbdULl9AOhmOR3K7hHasqWXwcOTbvaHr3HEEABGgQhe1HXvPjsLQD1oNkkbUwooliprhKe-5rw'
#calendly = Calendly(api_key)


url="https://api.calendly.com/scheduled_events?organization=https://api.calendly.com/organizations/CHHCQYYBK6CI5GMA"
#headers = {'content-type': 'application/soap+xml'}
headers1 = {'content-type': 'application/json','Authorization' : 'Bearer eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjk1NjI2NDE3LCJqdGkiOiJmNzEzZTQ5Ny03ZWJkLTQ0OTYtOTc3Ni03ZTdiMjk3NjlkMzkiLCJ1c2VyX3V1aWQiOiJHRUhIWFkyQ09QSklYWlI2In0.JVBCRR2z2kO6VbdULl9AOhmOR3K7hHasqWXwcOTbvaHr3HEEABGgQhe1HXvPjsLQD1oNkkbUwooliprhKe-5rw'}

#Loop thro 4 months and get all the events
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
        jsonData.to_csv('events.csv',index=False, encoding='utf-8')
    else:
        jsonData.to_csv('events.csv',header=False,mode='a',index=False, encoding='utf-8')

#read events csv
data1 = pd.read_csv('events.csv', index_col=0,keep_default_na=False )
headers1 = {'content-type': 'application/json','Authorization' : 'Bearer eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNjk1NjI2NDE3LCJqdGkiOiJmNzEzZTQ5Ny03ZWJkLTQ0OTYtOTc3Ni03ZTdiMjk3NjlkMzkiLCJ1c2VyX3V1aWQiOiJHRUhIWFkyQ09QSklYWlI2In0.JVBCRR2z2kO6VbdULl9AOhmOR3K7hHasqWXwcOTbvaHr3HEEABGgQhe1HXvPjsLQD1oNkkbUwooliprhKe-5rw'}
print(data1[['uri']].to_string(index=False))
data2 = pd.DataFrame()
i = 1
while i < len(data1):
  uri = data1.iloc[i].uri
  data2.loc[i,'meetingtime'] = data1.iloc[i].start_time
  data2.loc[i,'status'] = data1.iloc[i].status
  #get invitee details
  url = uri + '/invitees'
  response = requests.get(url=url,headers=headers1)
  df2 = json.loads(response.text)
  df2 = pd.json_normalize(df2["collection"])
  data2.loc[i,'email'] = df2['email'].to_string(index=False)
  data2.loc[i,'name'] = df2['name'].to_string(index=False)
  i = i+1
print(data2)
data2.to_csv('client_meeting.csv',index=False, encoding='utf-8')

data2 = pd.read_csv('client_meeting.csv',keep_default_na=False )

#read master client data
data3 = pd.read_csv('cdeclients.csv',keep_default_na=False )
data4 = pd.DataFrame()
j = 1

print(data3)
#data3 = data3.drop(data3[data3['ClientName'] in data2['name'].values].index)
i = 1
for i in range(len(data3)):
    data4.loc[i,'name'] = str(data3.iloc[i]['ClientName'])
    data4.loc[i,'ClassName'] = str(data3.iloc[i]['ClassName'])
    data4.loc[i,'Mobile'] = data3.iloc[i]['Mobile'].astype(str)
    data4.loc[i,'Meeting Date'] = ""
    data4.loc[i,'meetingstatus'] = ""
    #data4.loc[i,'status'] = str("Not Met")
    for j in range(len(data2)):
        if data3.iloc[i]['ClientName'] in data2.iloc[j]['name']:
            data4.loc[i,'Meeting Date'] = data2.iloc[j]['meetingtime']
            data4.loc[i,'meetingstatus'] = data2.iloc[j]['status']
            #data4.loc[i,'status'] = str("Met")
            break
data4.to_csv('clients_notmet.csv',index=False, encoding='utf-8')

