import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), r'C:\Users\Simeon\PycharmProjects\car_scraper_packages'))
from car_scraper.car_scraping_1 import Carscraper
import boto3
import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine


class DataHandling:
    # s3_client = boto3.client('s3')
    # DATABASE_TYPE = 'postgresql'
    # DBAPI = 'psycopg2'
    # HOST = 'aicoredb.cjpo05djrpn0.eu-west-2.rds.amazonaws.com'
    # USER = 'postgres'
    # PASSWORD = 'Orebach94*'
    # PORT = 5432
    # DATABASE = 'postgres'

    def __init__(self):
        self.carscraper = Carscraper()
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'
        self.HOST = 'aicoredb.cjpo05djrpn0.eu-west-2.rds.amazonaws.com'
        self.USER = 'postgres'
        self.PASSWORD = 'Orebach94*'
        self.PORT = 5432
        self.DATABASE = 'postgres'
        #self.cur = None
        self.df = None
        self.conn = psycopg2.connect(dbname=self.DATABASE, user=self.USER, password=self.PASSWORD, port=self.PORT, host=self.HOST)
        self.cur = self.conn.cursor()

    def load_csv(self):
        #with open(r"C:\Users\Simeon\PycharmProjects\pythonProject2\AiCore Substitute lecture videos & revision py_files\car_scraper package project 2\car_scraper\car_data_df.csv", 'r') as f:
            #self.cars_data_df = pd.read_csv(f, index_col=0)
        self.df = self.carscraper.print_to_json_and_csv()
        #self.df = pd.read_csv(df, index_col=0)
        #print(self.df)

    def create_rds_table(self):
        self.cur.execute("DROP TABLE IF EXISTS cars")
        self.cur.execute("CREATE TABLE cars (manufacturer VARCHAR(255), model VARCHAR(255), sale_price VARCHAR(255), year VARCHAR(255), transmission VARCHAR(255), fuel VARCHAR(255), mileage VARCHAR(255), condition VARCHAR(255), location VARCHAR(255), contact_number VARCHAR(255))")
        self.conn.commit()


    def store_data_in_database(self):
        engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}")
        engine.connect()
        self.df.to_sql('cars', engine, if_exists='replace', index=False)

    def query_database(self):
        self.cur.execute("SELECT * FROM cars")
        result = self.cur.fetchall()
        for r in result:
            print(r)
        self.conn.close()

    def run_data(self):
        self.load_csv()
        self.create_rds_table()
        self.store_data_in_database()
        self.query_database()

pushdata = DataHandling()

pushdata.run_data()

#######################################################################################################
#Adv method:
# def __init__(self, user, password, database, port, host):
#     self.user = user
#     self.password = password
#     self.database = database
#     self.port = port
#     self.host = host
#     self.carscraper = Carscraper()
#
#     global conn
# conn = psycopg2.connect(dbname=self.database, user=self.user, password=self.password, port=self.port, host=self.host)

# def __repr__(self):
#     return "User {0} connected to {1}.".format(self.user, self.database)

# @classmethod
# def get_credentials_and_login(cls, file_path):
#     with open(file_path, mode="r") as json_file:
#         # Store credentials to the global namespace
#         global credentials
#         credentials = json.load(json_file)
#
#     # login
#     return cls(credentials["user"],
#                credentials["password"],
#                credentials["database"],
#                credentials["host"])