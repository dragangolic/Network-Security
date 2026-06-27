from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Components.data_validation import DataValidation
from NetworkSecurity.Components.data_transformation import DataTransformation

from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Entity.config_entity import (
                DataIngestionConfig, DataValidationConfig, 
                TrainingPipelineConfig, DataTransformationConfig, 
                ModelTrainerConfig)
from NetworkSecurity.Components.model_trainer import ModelTrainer
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        logging.info("Starting data ingestion process")
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Starting data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
        
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Starting data transformation")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(data_transformation_artifact)

        logging.info("Model training started")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)