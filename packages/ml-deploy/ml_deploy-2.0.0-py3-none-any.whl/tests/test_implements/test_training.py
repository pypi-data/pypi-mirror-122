from tests.Training import UserModel

training = UserModel()

def test_training_task_metric_exists():
    assert 'training_task' in training.metric.metric_list()


def test_record_training():
    assert training.metric.record('training_task', value='running') == 'running'
    assert training.is_training()