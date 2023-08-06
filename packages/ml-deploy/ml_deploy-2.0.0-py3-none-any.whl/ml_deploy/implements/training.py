from abc import ABC, abstractmethod
import json


from ml_deploy.implements.base import BaseDeploy
from ml_deploy import metric
from ml_deploy import pipeline_config
from ml_deploy.validation.pipeline import DataValidation, ModelValidation
from ml_deploy.validation.exceptions import PipelineException

from flask_apscheduler import APScheduler
from prometheus_client import Enum
from multiprocessing import Process, Value


class Training(BaseDeploy, ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.setup_scheduler()
        Enum('training_task', 'State of training task', states=['running', 'rest'], registry=self.metric.registry)
        metric.record('training_task', value='rest')
        self.status_training = Value('i', False)


    def setup_scheduler(self):
        scheduler = APScheduler()
        self.scheduler = scheduler
        self.scheduler.init_app(self.app)
        self.scheduler.start()


    @abstractmethod
    def run_pipeline(self):
        pass


    # def is_training(self):
    #     training_state = self.metric.enum_state_value('training_task')
    #     if training_state == 'running':
    #         message = 'There is still another process of training'
    #         self.app.logger.info(message)
    #         return True
    #     return False

    
    def valid_input(self):
        data_config = pipeline_config.data
        if data_config.train_validation:
            if not hasattr(self, 'extraction'):
                raise PipelineException('Training pipeline need extraction method')
        return True


    def run_pipline_with_state(self):
        self.status_training.value = True
        self.run_pipeline()
        self.status_training.value = False


    def run_in_background(self, func):
        try :
            heavy_process = Process(  # Create a daemonic process with heavy "my_func"
            target = func,
                    daemon=True
                    
                )
            heavy_process.start()
        except :
            self.status_training.value = False
        
    
    def api_resources(self):
        super().api_resources()
        

        @self.app.after_request
        def after_request(response):
            self.after_request(response)
            try :
                data = json.loads(response.data)
                data = self.add_model_md(data)
                response.data = json.dumps(data)
                return response
            except :
                return response

                
        if self.app.config['SCHEDULER_API_ENABLED'] and hasattr(self, 'cron_datetime'):
            self.app.logger.info(f'Running scheduler at {str(self.cron_datetime)}')
            @self.scheduler.task('cron', id='train', **self.cron_datetime)
            def train_scheduler():
                is_training = self.status_training.value
                if is_training:
                    self.app.logger.info('There is still another process of training')
                else :
                    self.run_pipline_with_state()

        
        @self.app.route(f'{self.api_prefix_processed}/train', methods=['POST'])
        def api_train():
            is_training = self.status_training.value
            self.app.logger.debug(f'api train is training {is_training}')
            if is_training :
                message = 'There is still another process of training'
                self.app.logger.debug(message)
                return {'message' : message, 'status_code':200}, 200

            if hasattr(self, 'valid_pipeline') and not self.valid_pipeline():
                self.app.logger.debug('pipeline invalid')
                return {'message':'Input data is not valid', 'status_code':400}, 400
            
            if pipeline_config.model.background_training :
                self.app.logger.info('train model  in the background')
                self.run_in_background(self.run_pipline_with_state)
            else :
                self.app.logger.info('train model')
                try :
                    self.run_pipline_with_state()
                except Exception as e:
                    self.status_training.value = False
                    return {'message' : str(e), 'status_code':500}, 500
            return {'message' : 'Model is trained', 'status_code':200}