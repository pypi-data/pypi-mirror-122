# from ml_deploy.implements import BaseDeploy
# from ml_deploy import app_config
# from ml_deploy.utils import load_class
# from ml_deploy.rest.utils import check_return_model_md


# class Pipeline(BaseDeploy):
#     __name__ = None
#     __version__ = None


#     def __init__(self):
#         super().__init__()

    
#     def setup_md(self):
#         self.pipeline_name = check_return_model_md(self, None, '__name__')
#         self.pipeline_version = check_return_model_md(self, None, '__version__')


#     def run(self):
#         service = app_config.pipeline.service
#         if service == 'serving':
#             service = load_class(app_config.pipeline.serving)
#         elif service == 'training':
#             service = load_class(app_config.pipeline.training)

#         if self.mode == 'development':
#             service.dev_run()
#         elif self.mode == 'production' :
#             service.prod_run()