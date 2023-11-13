from datetime import datetime
from sqlalchemy import text
import pandas as pd
import datetime as dt
import requests

class dbmethods:

    def __init__(self,execute_engine,connection_link=str,connection_object=object,username=str):
        self.sql=connection_object
        self.engine=connection_link
        self.execute_engine=execute_engine
        self.tables=self.sql.tables
        self.user=username

    def get_current_datetime(self):

        return datetime.today()



    def fetch_tables(self,table_name=str,index_col=None):
        """
            Function to fetch all the data from table
        """
        try:
            df=pd.read_sql_table(table_name,self.engine)
            return df
        except Exception as e:
            print(e)

    def fetch_table_u(self,table_name=str):
        """
            Retrives the tables data w.r.t user
        """
        s="SELECT * FROM `"+table_name+"` WHERE username='"+str(self.user)+"'"
        try:
            df=pd.read_sql_query(s,self.engine)
            return df
        except Exception as e:
            print(e)

    def upload_to_table(self,df=pd.DataFrame(),table_name=str,if_exists=str):
        """
            Uploads dataframe to table
        """
        try:
            df.to_sql(table_name,con=self.engine,if_exists=if_exists,index=0)
            return True
        except Exception as e:
            print(e)
            return False


    def upload_meeting_data(self,df=pd.DataFrame(),table_name=str,if_exists=str):
        start_time=df.reset_index().head(1)['meetingtime']
        print(start_time)
        print(self.engine)
        q="DELETE FROM `"+str(table_name)+"` WHERE meetingtime < '"+str(start_time)+"';"
        try:
            try:
                self.fetch_query(q)
            except:
                pass
            df.to_sql(table_name,con=self.engine,if_exists=if_exists,index=0)
            return True
        except Exception as e:
            print(e)
            return False

    
    def send_reminder(self,customer_name=str,number=str,token=str,template_id=str):

        
        contact_no=number
        
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
            return 1,'',current_time
        
        except Exception as e:
            print(e)
            print("Response : Error to send reminder!")
            return 0,e,0

    def send_customers_reminders(self,df=pd.DataFrame(),table_name=str,token=str,template_id=str):
        print(df)
        for i in range(len(df)):
            df['Mobile']=df['Mobile'].astype('int')
            classname = df.iloc[i]['ClassName']

            customer_name_1 = df.iloc[i]['ClientName']
            contact2 = df.iloc[i]['Mobile'].astype('str')
            print(contact2)
            contact2 = contact2.replace(".0","")
            if contact2.startswith("91"):
                modified_string = contact2[2:]

            print(customer_name_1,contact2,classname)
            currenttime=dt.datetime.now()
            #contact2=data.iloc[i]['contact_number'].astype(str)
            try:
                #status,message,remindertime=self.send_reminder(customer_name=customer_name_1,number=contact2,token=token,template_id=template_id)
                #status=1
                if status:
                    update_status,mes=self.update_reminder_date(customer_name=customer_name_1,contact_no=contact2,table_name=table_name,remindertime=currenttime,classname=classname)
                    if update_status:
                        return 1,''
            except Exception as e:
                print(e)
                return 0,e

    def update_reminder_date(self,customer_name,contact_no,table_name,remindertime,classname):
        
        data={'name':customer_name,'ClassName':classname,'Mobile':contact_no,'reminderdate':remindertime}
        df=pd.DataFrame([data])
        try:
            df.to_sql(table_name,con=self.engine,if_exists="append",index=0)
            return 1,''
        except Exception as e:
            print(e)
            return 0,e   
            
    def fetch_query(self,query=str):
        #try:
        self.engine.execute(text(query))

        #return pd(sql=query,con=self.engine)
        #except Exception as e:
        #    print(e)
        #    return 0
        
    def update_row(self,table_name=str,update_values=dict,where_col=str,where_col_value=str):
        #sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
        update_string=''
        count=0
        for i,k in update_values.items():
            count+=1
            if count<len(update_values):
                update_string = update_string+str("{} = '{}', ".format(i,k))
            elif count==len(update_values):
                update_string= update_string+str("{} = '{}' ".format(i,k))

        update_q="UPDATE `"+table_name+"` SET "+update_string+" WHERE "+where_col+" = '"+where_col_value+"'"
    
        #try:
        self.engine.execute(text(update_q))
        return 1
        #except Exception as e:
        #    print(e)
        #    return 0
            
    def fetch_customers_names(self):
        try:
            return self.fetch_tables(table_name=self.tables["customer_table"])["name"].drop_duplicates()
        except:
            return 0

    def fetch_customer(self,customer_name=str):
        customer_tbl=self.tables["customer_table"]
        query="SELECT * FROM `"+customer_tbl+"` WHERE name='"+customer_name+"'"
        try:
            return pd.read_sql_query(sql=query,con=self.engine)
        except:
            return 0

    def update_customer(self,update_values=dict,customr_name=str):
        where_col='name'
        return self.update_row(table_name=self.tables["customer_table"],update_values=update_values,where_col=where_col,where_col_value=customr_name)


    def fetch_access_tokens(self,table_name=str):
        """
            To fetch all access tokens
        """
        query_names_q='SELECT id,access_token,createdate FROM `'+ table_name+'`'
        query_names_df=pd.read_sql_query(query_names_q,self.engine,index_col=['id']).drop_duplicates().dropna(axis=1,how='all')
        if len(query_names_df):
            query_names_df=query_names_df.sort_values(by='createdate',ascending=False,ignore_index=True)
            return query_names_df
        else:
            return pd.DataFrame()

    def update_access_token(self,access_token=str,api_key=str,api_secret=str):
        """
            To fetch all access tokens
        """
        current_time=datetime.now()
        table_name=self.tables["access_token_table"]
        df=pd.DataFrame(data={'id':1,'api_key':api_key,'api_secret':api_secret,'access_token':access_token,'createdate':current_time},index=[0])
        df.to_sql(table_name,self.engine,if_exists="replace",index=False)
           
    

    def get_order_log_names(self):
        order_table=self.tables['order_log_table']
        query = "SELECT customerusername FROM '"+order_table+"'"
        return self.fetch_query(query=query)

    def get_order_log(self,username=str,label=None):
        order_table=self.tables['order_log_table']
        if label!="admin":
            s="SELECT * FROM `"+order_table+"` WHERE customerusername='"+str(username)+"'"
            return self.fetch_query(query=s)
        else:
            return self.fetch_tables(order_table)
            
    def delete_row(self,table_name=str,condition=str):
        d="DELETE FROM `"+table_name+"` WHERE '"+condition+"'"
        print(d)
        #try:
        self.engine.execute(text(d))
        #except Exception as e:
        #    print(e)

    def update_cutomer_status(self,customer_name=str,update_dic=dict):
        customer_tbl=self.tables["customer_table"]
        #uq="UPDATE `"+customer_tbl+"` SET status="+str(status)+" Where name='"+str(customer_name)+"'"
        #print(uq)
        self.update_row(table_name=customer_tbl,update_values=update_dic,where_col='name',where_col_value=customer_name)
        #except Exception as e:
        #    print(e)
       
    def check_customer(self,name=str,angel_user=str):
        customer_tbl=self.tables["customer_table"]
        acc_query = "SELECT * FROM `"+customer_tbl+"` where name='"+name+"' and angel_user='" + angel_user + "'"
        print(self.fetch_query(acc_query))
        return self.fetch_query(acc_query)

    def encrypt_password(self,password=str):
        encryption_key=self.encryption_key
        return Fernet(encryption_key).encrypt(password.encode())

    def decrypt_password(self,password=bytes):
        encryption_key=self.encryption_key
        return Fernet(encryption_key).decrypt(password).decode()

    def upload_passwords(self,password=bytes,customr_name=str):
        #using customer_temp table to update the blob column in customer
        #delete customer_temp records
        query="DELETE FROM customer_temp"
        
        self.engine.execute(text(query))
        #insert encrypted password to customer_temp using dataframe
        dic={"temppwd": password}
        
        df=pd.DataFrame(dic,index=[0])

        self.upload_to_table(df=df,table_name=self.tables["customer_temp_table"],if_exists="append")

        query="UPDATE customer SET angel_pwd = (SELECT temppwd FROM customer_temp) where name='"+customr_name+"'"
        
        self.engine.execute(text(query))
        
    def update_set_values(self,data=dict,if_exist=str):
        '''
            This method is used to update the set values of defaults table.
            -data=dict,
            example:
                data={'name':varaible_name,'value':variable_value}
        '''
        set_values_tbl=self.tables['defaults_table']
        
        #data['createdate']=self.get_current_datetime()

        df=pd.DataFrame(data=data,index=[0])

        try:

            return self.upload_to_table(df,set_values_tbl,if_exist)

        except Exception as e:

            print(e)

    def decrypt_password(self,password=bytes):
        print(password)
        encryption_key=self.encryption_key
        print(Fernet(encryption_key).decrypt(password).decode())
        return Fernet(encryption_key).decrypt(password).decode()
    
    def order_report(self,table_name=str):
        order_query="select customerusername, DATE(createdate) date1, SUM(pnl) from order_log GROUP BY date1,customerusername"
        df=self.fetch_query(order_query)
        return df
