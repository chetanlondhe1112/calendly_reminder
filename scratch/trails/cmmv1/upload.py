import requests
import pandas as pd
import json
from connection.db_conn import sqlalchemy_connect
from connection.db_methods import dbmethods

def sq():
    """Database connection and database method collecting from object"""
    return sqlalchemy_connect()

sql=sq()

tables_dict=sql.read_config()

db_tables=tables_dict["db_tables"]
print(sql.engine)
clients_data_tbl=db_tables["clients_data_table"]
clients_notmet_data_tbl=db_tables["clients_notmet_data_table"]
meeting_data_tbl=db_tables["meeting_data_table"]


dbm=dbmethods(connection_link=sql.engine(),connection_object=sql,username='chetan')

print(dbm.fetch_tables(table_name=clients_data_tbl))
df=pd.read_csv("F:/Project-11/calendly_reminder/scratch/trails/cmmv1/clients_notmet.csv",index_col=None)
dbm.upload_to_table(df=df,table_name=clients_notmet_data_tbl,if_exists="replace")
