from ml_deploy.validation.config import DataConfig, ModelConfig
from ml_deploy.validation.exceptions import DataValidationException

from typing import Union
from pydantic import BaseModel
import copy
import numpy as np
from ml_deploy.mlflow import log_model, log_built_in_flavor_model


class DataValidation(BaseModel):
    config: DataConfig

    def valid_features(self, features:list)->dict:
        config = self.config

        feature_names = [ feature.name for feature in config.features ]
        unexpected = [ feature for feature in features if feature not in feature_names ]
        if unexpected :
            raise DataValidationException(f'Unexpected features {unexpected}')

        required = [ feature for feature in feature_names if feature not in features ]
        if required :
            raise DataValidationException(f'Input required these features {required}')

        if features != feature_names:
            raise DataValidationException(f'Input may not in correct order')

        return True

    
    def valid_values(self, data:Union[np.ndarray, list]):
        data = self.parse_dtypes(data)
        if self.value_accepted(data):
            return data
        return False


    def parse_dtypes(self, data:Union[np.ndarray, list]):
        """
        If datatype is list, convert it to numpy.
        convert data type in every feature
        """
        data = copy.deepcopy(data)
        if type(data) == list :
            data = np.array(data)
        elif type(data) != np.ndarray:
            raise DataValidationException(f'Data for validation must be in the type of np.ndarray or list')
        
        # convert data type in every feature
        config = self.config
        n_feature = data.shape[1]
        for i in range(n_feature):
            dtype = config.features[i].dtype
            if dtype is not None :
                data[:, i] = data[:, i].astype(dtype)
        return data

    
    def valid_range(self, feature_data:np.ndarray, feature_conf:dict):
        values_conf = feature_conf.values
        min_value = values_conf.get('min', None)
        max_value = values_conf.get('max', None)
        min_value = values_conf.get('min', None)
        exceed_max = max_value is not None and feature_data.max() > float(max_value)
        less_min = min_value is not None and feature_data.min() < float(min_value)
        if exceed_max or less_min :
            raise DataValidationException(f"Feature '{feature_conf.name}' value exceed max or less than min")
        return True


    def value_expected(self, feature_data, feature_conf:list):
        values_conf = feature_conf.values
        sum_not_member = sum(~np.isin(feature_data, values_conf))
        if sum_not_member > 0 :
            raise DataValidationException(f"Feature '{feature_conf.name}' has Unexpected categorical value. expected values are {values_conf}")
        return True

    
    def value_accepted(self, data:np.ndarray)->bool:
        config = self.config
        for i, feature_conf in enumerate(config.features) :
            values_conf = feature_conf.values
            if values_conf is not None and type(values_conf) == dict :
                # check min and max
                feature_data = data[:, i]
                self.valid_range(feature_data, feature_conf)
            elif values_conf is not None and type(values_conf) == list :
                feature_data = data[:, i]
                self.value_expected(feature_data, feature_conf)
        return True


class ModelValidation(BaseModel):
    config: ModelConfig



    def compare_performance(self, comparation, new_score, curr_score):
        if comparation == 'lt':
            return new_score < curr_score
        elif comparation == 'gt':
            return new_score > curr_score
        elif comparation == 'lte':
            return new_score <= curr_score
        elif comparation == 'gte':
            return new_score >= curr_score


    def valid_performance(
        self, 
        model, 
        test_func, 
        x, 
        y, 
        curr_model=None, 
        log_to_mlflow:bool=False,
        flavor_name:str=None,
        arifact_path:str='model',
        registered_model_name:str='Model',
        as_production=True,
        *args, **kwargs
        )->bool:

        performance = self.config.performance
        benchmark = performance.benchmark
        on_curr_model_conf = performance.on_curr_model
        new_model_score = test_func(model, x, y, *args, **kwargs)

        is_better = False
        
        # if current model is None, set vali performance
        if curr_model is None:
            is_better = True
        elif on_curr_model_conf.validate or benchmark.validate :
            # compare performance between new model score and benchmark score
            better_than_benchmark = self.compare_performance(benchmark.comparation, 
                                        new_model_score, benchmark.value) if benchmark.validate else True

            # compare performance between new model score and current model score
            prod_model_score = test_func(curr_model, x, y)
            better_than_curr_model = self.compare_performance(on_curr_model_conf.comparation, 
                                        new_model_score, prod_model_score) if on_curr_model_conf.validate else True
            if better_than_curr_model and better_than_benchmark:
                is_better = True
            else :
                is_better = False
        else :
            is_better = True

        if is_better and log_to_mlflow :
            if flavor_name is None :
                log_model(model, arifact_path, registered_model_name=registered_model_name, as_production=as_production)
            else :
                log_built_in_flavor_model(flavor_name, model, arifact_path, registered_model_name, curr_production_model=True)

        return is_better