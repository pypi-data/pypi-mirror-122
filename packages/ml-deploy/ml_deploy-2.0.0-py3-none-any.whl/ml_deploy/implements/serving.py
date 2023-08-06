import json
import time
from abc import ABC, abstractmethod

from ml_deploy.implements.base import BaseDeploy
from ml_deploy.kafka.utils import send_messages, topic_add_or_create
from ml_deploy.rest.utils import get_all_request
from ml_deploy.errors import ModelMethodRequired
from ml_deploy.validators import RequestPredict, Response
from flask import request, g

class Serving(BaseDeploy, ABC):
    
    def __init__(self) -> None:
        if not hasattr(self, 'predict'):
            ModelMethodRequired('Predict method is required')
        super().__init__()

    
    @abstractmethod
    def load(self):
        pass


    def add_model_md(self, data):
        data['model'] = self.model_name
        data['version'] = self.model_version
        return data


    def api_resources(self):
        super().api_resources()

        @self.app.after_request
        def after_request(response):
            self.after_request(response)
            try :
                data = json.loads(response.data)
                data = self.add_model_md(data)
                if self.producer is not None : # send message to broker, if broker provided
                    send_messages(self.producer, data)

                response.data = json.dumps(data)
                return response
            except :
                return response


        @self.app.route(f'{self.api_prefix_processed}/predict', methods=['POST'])
        def predict():
            # get data requests
            req_data = get_all_request()
            # req_data = RequestPredict(**req_data)
            
            result = self.predict(req_data)

            # provide topic data
            if self.producer is not None :
                result = topic_add_or_create(result, ['predict'])

            return result
            

        if hasattr(self, 'feedback'):
            @self.app.route(f'/{self.api_prefix_processed}/feedback', methods=['POST'])
            def feedback():
                # get data requests
                data = get_all_request()
                input_data = data.pop('data')
                y_true = data.get('y_true')
                y_predicted = data.get('y_predict', None)

                result = self.feedback(input_data, y_true, y_predicted)

                # provide topic data
                if self.producer is not None :
                    result = topic_add_or_create(result, ['feedback'])

                return result