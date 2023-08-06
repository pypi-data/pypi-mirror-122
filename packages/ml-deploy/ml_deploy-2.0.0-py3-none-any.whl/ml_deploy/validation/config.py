from ml_deploy.validation.utils import is_file_exists

from typing import List, Union, Optional

from pydantic import validator, BaseModel


class AppConfig(BaseModel):
    interface:str
    metric_class:str = None
    kafka_broker:str = None
    http_port:int = 5000
    mode:str = 'development'
    debug:bool = True
    log_level:str = 'INFO'
    workers:int = 1
    worker_class:str = 'sync'
    gunicorn_timeout:int = 5000
    threads:int = 5
    max_requests:int = 0
    max_requests_jitter:int = 0
    keepalive:int = 2


    @validator('interface')
    def option_interface_value(cls, v):
        if not is_file_exists(v):
            ValueError(f'interface file is not exists {v}')
        return v

    
    @validator('metric_class')
    def option_metric_value(cls, v):
        if not is_file_exists(v):
            ValueError(f'Metric file is not exists {v}')
        return v

    @validator('mode')
    def option_mode_value(cls, v):
        option = ['development', 'production']
        if v not in option:
            ValueError(f'Mode value must be one of this {option}')
        return v


class FeatureConfig(BaseModel):
    name:str
    dtype:Optional[str] = None
    values:Union[list, dict] = None


class DataConfig(BaseModel):
    train_validation:bool = False
    prediction_validation:bool = False
    features:List[FeatureConfig] = []


class ModelParamsConfig(BaseModel):
    validation:bool = False
    config:dict = {}


class PerformanceConfig(BaseModel):
    validation:bool = True
    comparation:str = 'gt'
    value:float = 0.0


class ModelPerformanceConfig(BaseModel):
    on_curr_model:PerformanceConfig
    benchmark:PerformanceConfig


class ModelConfig(BaseModel):
    config:ModelParamsConfig
    performance:ModelPerformanceConfig
    background_training:bool=True
    

class AllConfig(BaseModel, extra='allow'):
    app: AppConfig
    data: Optional[DataConfig] = None
    model: Optional[ModelConfig] = None