from ml_deploy.metrics.models import Metric
from prometheus_client import Enum

metric = Metric()

def test_enum():
    assert Enum == metric.metric_type['ENUM']
    assert metric.method_type[Enum] == 'state'