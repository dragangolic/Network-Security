import os, sys

from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging

from NetworkSecurity.Entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from NetworkSecurity.Entity.config_entity import ModelTrainerConfig

from NetworkSecurity.Utils.Main_utils.utils import save_object, load_object
from NetworkSecurity.Utils.Main_utils.utils import load_numpy_array_data, evaluate_models
from NetworkSecurity.Utils.Ml_utils.Model.estimator import NetworkModel
from NetworkSecurity.Utils.Ml_utils.Metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,GradientBoostingClassifier, RandomForestClassifier
)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, 
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regresion": LogisticRegression(verbose=1),
            "Adaboost": AdaBoostClassifier()
        }
        params = {
            "Decision Tree": {
                "criterion": ['gini', 'entropy', 'log_loss'],
                # 'splitter':['best', 'random'],
                # 'max_features':['sqrt', 'log2'],
            },
            "Random Forest": {
                "n_estimators": [8,16,32,64,128,256],
                # "criterion": ['gini', 'entropy', 'log_loss']
                # 'max_features':['sqrt', 'log2', None]
            },
            "Gradient Boosting": {
                "learning_rate": [.1, .01, .05, .001],
                "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                "n_estimators": [8,16,32,64,128,256],
                # 'loss': ['log_loss', 'exponential']
            },
            "Logistic Regresion": {},
            "Adaboost": {
                "learning_rate": [.1, .01, .05, .001],
                "n_estimators": [8,16,32,64,128,256],
            }
        }
        model_report: dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                             models=models, param=params)
        # To get the best model score from dict
        best_model_score = max(sorted(model_report.values()))

        # To get best model score from dict
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformation_train_file_path
            test_file_path = self.data_transformation_artifact.transformation_test_file_path

            # Loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )
            model = self.train_model(X_train, y_train)

        except Exception as e:
            raise NetworkSecurityException(e, sys)