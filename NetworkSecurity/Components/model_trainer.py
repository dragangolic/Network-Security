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
import mlflow


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, 
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def track_mlflow(self, best_model, classificationmetric):
        with mlflow.start_run():
            f1_score = classificationmetric.f1_score
            precision_score = classificationmetric.precision_score
            recall_score = classificationmetric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision_score)
            mlflow.log_metric("recall", recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=0),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=0),
            "Logistic Regresion": LogisticRegression(verbose=0),
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
                "learning_rate": [0.01, .01],
                "subsample": [0.8, 1.0],
                "n_estimators": [50, 100],
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
        y_train_pred = best_model.predict(X_train)

        classification_train_metric = get_classification_score(y_true = y_train, y_pred = y_train_pred)

        ## Track the experiments with mlflow
        self.track_mlflow(best_model, classification_train_metric)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        # self.track_mlflow(best_model, classification_test_metric)


        preprocessor = load_object(file_path=self.data_transformation_artifact.transformation_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=NetworkModel)

        # MOdel trainer artifact
        model_trainer_artifact = ModelTrainerArtifact(
                            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                            trained_metric_artifact=classification_train_metric,
                            test_metric_artifact=classification_test_metric
                             )
        logging.info(f"MOdel trainer artifact: {model_trainer_artifact}") 
        return model_trainer_artifact

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
            model = self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys)