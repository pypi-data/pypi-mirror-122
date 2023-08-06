

def test_registry(base_deploy_instance):
    serving = base_deploy_instance
    assert hasattr(serving.metric, 'registry')


def test_metric_instance(base_deploy_instance):
    serving = base_deploy_instance
    assert 'request_timer' in serving.metric.metric_list()
    assert 'request_counter' in serving.metric.metric_list()

    

    
    