from prometheus_client import (
    Counter, Histogram, Gauge, Enum,
    CollectorRegistry, 
    generate_latest
    )
import copy


class Metric:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.init_software_metrics()
        self.metric_func = {}
        self.metric_type = {
            'GAUGE' : Gauge,
            'COUNTER': Counter,
            'TIMER' : Histogram,
            'ENUM' : Enum
        }
        self.method_type = {
            Gauge : 'set',
            Counter: 'inc',
            Histogram : 'observe',
            Enum : 'state'
        }
        if hasattr(self, 'register'):
            self.register_metrics()
        


    def init_software_metrics(self):
        Histogram('request_timer', 'Time spent processing request', labelnames=['method', 'endpoint', 'status', 'model', 'version'], registry=self.registry)
        Counter('request_counter', 'Count number of request', labelnames=['method', 'endpoint', 'status', 'model', 'version'], registry=self.registry)



    def get_metric(self, name):
        all_collector = copy.copy(self.registry._collector_to_names)
        for metric in all_collector:
            if metric._name == name :
                return metric
        return None


    def metric_list(self):
        all_collector = copy.copy(self.registry._collector_to_names)
        return [ metric._name for metric in all_collector ]



    def generate_metrics(self):
        return generate_latest(self.registry)



    def record(self, name, dim_vals=[], params={}, value=None):
        metric = self.get_metric(name)
        if not metric :
            raise ValueError('Metric name is not exists')

        if not value :
            if name not in list(self.metric_func.keys()):
                raise ValueError('Metric name is not exists')
            value = self.metric_func[name](**params)

        if len(dim_vals) == len(metric._labelnames):
            self._update_metric(metric, dim_vals, value)
        else :
            raise ValueError('Some label value is not provided')

        return value


    def _update_metric(self, metric, dim_vals, value):
        metric_class = metric.__class__
        if dim_vals:
            labeled_metric = metric.labels(*dim_vals) if type(dim_vals) == list else metric.labels(**dim_vals)
        else :
            labeled_metric = metric

        getattr(labeled_metric, self.method_type[metric_class])(value)


    def metric_value(self, name):
        return self.get_metric(name)._value

    
    def enum_state_value(self, enum_name):
        metric = self.get_metric(enum_name)
        value = self.metric_value(enum_name)
        return metric._states[value]


    def register_metrics(self):
        for metric in self.register():
            name = metric.get('name', metric['function'].__name__)
            labelnames = metric.get('dimension', [])
            description = metric.get('description', getattr(metric['function'], '__doc__', ''))
            if metric not in self.metric_list():
                self.metric_type[metric['type']](
                    name, description, labelnames=labelnames, registry=self.registry
                    )
                self.metric_func[name] = metric['function']