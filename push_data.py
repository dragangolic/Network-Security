import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging 

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL= os.getenv("MONGO_DB_URL")
print(f"MONGO_DB_URL: {MONGO_DB_URL}")

ca= certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def cv_json_convertor(self, file_path):
        try:
            data= pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            return data.to_dict(orient="records")
            #records= list(json.loads(data.T.to_json()).values())
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database= database
            self.collection= collection
            self.records= records

            self.mongodb_client= pymongo.MongoClient(MONGO_DB_URL)
            self.database= self.mongodb_client[self.database]

            self.collection= self.database[self.collection]
            
            #print(type(self.records))
            #print(len(self.records) if self.records else "No records")
            #print(self.records[:3] if self.records else "Empty")
            
            print(f"Number of records: {len(self.records)}")
            self.collection.insert_many(self.records[:100])
            #self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__=="__main__":
    FILE_PATH = "Network_Data/dataset_10k.csv"
    DATABASE = "NetworkSecurity"
    COLLECTION = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_json_convertor(FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)