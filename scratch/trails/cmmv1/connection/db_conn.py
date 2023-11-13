from datetime import datetime
from sqlalchemy import create_engine
import time
import tomlkit

#config_file_path="config/tls_config.toml"
config_file_path="F:/Project-11/calendly_reminder/scratch/trails/cmmv1/config/config.toml"

class sqlalchemy_connect:

    def __init__(self):
        self.file_path=config_file_path
        self.config=self.read_config()
        self.cred=self.config['db_server']
        self.tables=self.config['db_tables']
        #self.engine=self.engine()
       
    def now_time(self):
      """
        To get the current time in datetime format
      """
      curr_time = datetime.now()
      
      return str(curr_time).split(".")[0]

    def read_config(self):
        """
            Generates the connection for database
        """
        print(str("\n"+self.now_time())+" = Reading Configuration File....")
        time.sleep(1)
        try:
            with open(self.file_path, mode="rt", encoding="utf-8") as fp:
                config=dict(tomlkit.load(fp))
                print("\n"+str(self.now_time())+" = Configuration File Read: Success :)")
                #self.config_info(config)
                return config
        except Exception as e:
            print("\n"+str(self.now_time())+" = Configuration File Read: Failed :(")
            time.sleep(2)
            print(e)

    def read_tables(self):
        """
            Returns all tabls of database
        """
        return self.tables

    def config_info(self,configuration=dict):
        """
            Reads The Configuration file
        """
        print("\n"+str(self.now_time())+" = Collecting File Information...")
        time.sleep(1)
        print("="*50)
        time.sleep(1)
        print("Name: "+str(configuration['file_info']['file_name']))
        print("Info: "+str(configuration['file_info']['info']))
        print("Version: "+str(configuration['file_info']['version']))
        time.sleep(1)
        print("*"*22+"Auther"+"*"*22)
        print("Auther Name: "+str(configuration['auther']['name']))
        print("Auther Mail: "+str(configuration['auther']['mail']))
        print("="*50)
        time.sleep(1)

    def sqlalchemy_connection(self,credential_dict=dict):
        """
        function to establish the sqlalchemy connection to the database
        -credential_dict = dict|Argument passed to function should be the dictionary of database configuration
        """
        user=credential_dict["user"]
        password=credential_dict["password"]
        host=credential_dict["host"]
        port=credential_dict["port"]
        database=credential_dict["database"]
        status_str=" = Connection Object Build :"

        print(str(self.now_time())+" = Generating Connection Object...")
        time.sleep(1)
        try:
            engine=create_engine("mysql://{}:{}@{}:{}/{}".format(user,password,host,port,database))
            print(str(self.now_time())+status_str+"Success")
            #print(str(self.now_time())+" = Connection Object :"+str(engine))
            time.sleep(1)
            return engine
        except Exception as e:
            print(str(self.now_time())+status_str+"Failed")
            print(str(self.now_time())+" = Error : "+str(e))
            return ''

    def engine(self):
        """
          Function to create the connection with database
        """
        return self.sqlalchemy_connection(self.cred)

    def engine_conn(self):
        """
          Function to create the connection with database
        """
        return self.engine().connect()

    