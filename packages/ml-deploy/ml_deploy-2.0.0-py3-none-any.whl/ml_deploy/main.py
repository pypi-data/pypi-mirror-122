import sys, os
from ml_deploy.utils import load_class
from ml_deploy import app_config

sys.path.append(os.getcwd())

def main():
    interface_name = app_config.interface_name
    user_class = load_class(interface_name)
    user_model = user_class()
    user_model.api_resources()
    user_model.run()

if __name__ == '__main__':
    main()