from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging

## Configuration of the Data Ingestion Config
from NetworkSecurity.Entity.config_entity import DataIngestionConfig
from NetworkSecurity.Entity.artifact_entity import DataIngestionArtifact
import os, sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
        except Exception as e:
            raise NetworkSecurityException(e, sys) 

    def export_collection_as_dataframe(self):
        '''Read data from MongoDB'''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            
            collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace(to_replace="na", value=np.nan, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys) 

    
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataset")
            logging.info("Exit from the split_data_as_train_test method of DataIngestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)    
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)   
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Exported training and testing dataset into feature store")

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
    