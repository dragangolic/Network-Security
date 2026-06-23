from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        logging.info("Starting data ingestion process")
        data_ingestion = DataIngestion(dataingestionconfig)
        
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionconfig)

    except Exception as e:
        raise NetworkSecurityException(e, sys)