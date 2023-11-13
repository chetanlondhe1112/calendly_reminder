import pandas as pd
import requests
import pdb
import datetime as dt

#Read customers csv
data = pd.read_csv('clients_notmet.csv',keep_default_na=False )

pdb.set_trace()
customer_name = ""
contact2 = ""

print(data)

df = pd.DataFrame()
#Loop thro each customer
for i in range(len(data)):
    if i > 25:
        if data.iloc[i]['meetingstatus'] == "":
            print("Not met")
            print(i," ",data.iloc[i]['name'])
            print(i," ",data.iloc[i]['Mobile'])
            ist_datetime = dt.datetime.now()
            current_time = ist_datetime.strftime("%m/%d/%Y, %H:%M:%S")
            df.loc[i,'Name'] = data.iloc[i]['name']
            df.loc[i,'Mobile'] = data.iloc[i]['Mobile']
            df.loc[i,'ClassName'] = data.iloc[i]['ClassName']
            df.loc[i,'Createdate'] = current_time
    if i > 50:
        break

df.to_csv('clients_25to50.csv',index=False, encoding='utf-8')

