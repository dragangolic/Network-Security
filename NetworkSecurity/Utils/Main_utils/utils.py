import yaml
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import  logging
import os, sys
import numpy as np
import dill
import pickle
from sklearn.metrics import f1_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.base import clone


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exist(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    '''
    Save numpy array data to file 
    file_path: str location of file to save 
    array: np.array data to save
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of Mainutils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of Mainutils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path: str,) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exests")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e 
    
def load_numpy_array_data(file_path: str) -> np.array:
    '''
    Load numpy array data from file file_path: str location of the file 
    to load return: np.array data loaded
    '''
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        best_model = None
        best_model_score = -1
        best_model_name = None

        for name, model in models.items():
            model = clone(model)
            para = param.get(name, {})

            gs = RandomizedSearchCV(
                model,
                para,
                cv=3,
                n_iter=5,
                n_jobs=-1,
                random_state=42
            )

            gs.fit(X_train, y_train)

            current_model = gs.best_estimator_

            y_train_pred = current_model.predict(X_train)
            y_test_pred = current_model.predict(X_test)

            train_score = f1_score(y_train, y_train_pred)
            test_score = f1_score(y_test, y_test_pred)

            report[name] = test_score

            # track best model
            if test_score > best_model_score:
                best_model_score = test_score
                best_model = current_model
                best_model_name = name

        return report, best_model, best_model_name

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e