from flask import Flask
from flask_cors import CORS
from ml_deploy.kafka.utils import create_producer
from ml_deploy.metrics import Metric
from ml_deploy.utils import load_class, get_args
import os, sys

sys.path.append(os.getcwd())

app_config, pipeline_config = get_args()

app = Flask(__name__)
CORS(app)

producer = create_producer(app_config.kafka_broker) if app_config.kafka_broker is not None else None
metric_class = getattr(app_config, 'metric_class', None)
metric_class = load_class(metric_class) if metric_class else Metric
metric = metric_class()