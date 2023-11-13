import pandas as pd
import requests
import pdb
import datetime as dt
from datetime import date

wh_token="73bd2696deeaf0acafbb5d4264505d20c70de546"
wh_template_id="PJ5892440"
#Read customers csv
data = pd.read_csv('clients_25to50.csv',keep_default_na=False )

customer_name = ""
contact2 = ""
def send_meeting_reminder(customer_name=customer_name,number=contact2,token=str,template_id=str):
    
    contact_no=contact2
    
    url = "https://pickyassist.com/app/api/v2/push"

    ist_datetime = dt.datetime.now()

    current_time = ist_datetime.strftime("%m/%d/%Y, %H:%M:%S")

    payload = "{\"token\":\""+str(token)+"\",\
                \"application\":8,\
                \"template_id\":\""+str(template_id)+"\",\
                \"data\":[ { \
                \"number\":\""+str(contact_no)+"\",\
                \"template_message\":[\""+str(customer_name)+"\"],\
                \"language\":\"en\"}]}"
    print(payload)
    
    headers = {'content-type': "application/json"}
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        print("Response : ",response.text)
        return 1
    
    except Exception as e:
        print(e)
        print("Response : Error to send reminder!")
        
        return 0


print(data)

df = pd.DataFrame()
#Loop thro each customer

for i in range(len(data)):
    customer_name_1 = data.iloc[i]['Name']
    contact2 = data.iloc[i]['Mobile'].astype(str)
    contact2 = contact2.replace(".0","")
    print(customer_name_1,contact2)
	#contact2=data.iloc[i]['contact_number'].astype(str)
    status=send_meeting_reminder(customer_name=customer_name_1,number=contact2,token=wh_token,template_id=wh_template_id)
    print(status)
    pdb.set_trace()
    ist_datetime = dt.datetime.now()
    current_time = ist_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    df.loc[i,'Name'] = data.iloc[i]['Name']
    df.loc[i,'Mobile'] = data.iloc[i]['Mobile']
    df.loc[i,'ClassName'] = data.iloc[i]['ClassName']
    df.loc[i,'Createdate'] = current_time

today = date.today()
filename = "client_reminder_sent" + str(today) + ".csv"
df.to_csv(filename,index=False, encoding='utf-8')

