from NetworkSecurity.Entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from NetworkSecurity.Entity.config_entity import DataValidationConfig
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os, sys
from NetworkSecurity.Utils.Main_utils.utils import read_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)