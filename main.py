from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Components.data_validation import DataValidation
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Entity.config_entity import DataIngestionConfig, DataValidationConfig, TrainingPipelineConfig
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        logging.info("Starting data ingestion process")
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionconfig)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionconfig, data_validation_config)
        logging.info("Starting data validation")
        data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_config)

    except Exception as e:
        raise NetworkSecurityException(e, sys)