from NetworkSecurity.Entity.artifact_entity import DataValidationArtifact
from NetworkSecurity.Entity.config_entity import DataValidationConfig
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os, sys
