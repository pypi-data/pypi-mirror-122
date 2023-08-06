import os
from sys import version
from numpy.lib.index_tricks import OGridClass
import requests

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.exceptions import MlflowException
from mlflow.utils.file_utils import TempDir
from requests.exceptions import ConnectionError


client = MlflowClient()
HOST = os.environ.get('MLFLOW_TRACKING_URI', None)


def test_connection_is_fail():
    try :
        client = MlflowClient()
        client.list_experiments()
        print('Connect to MLFLOW')
        return False
    except Exception as e :
        if e.__class__ == ConnectionError:
            return True
        return False

if HOST is not None and test_connection_is_fail():
    raise MlflowException('Are you trying to connect to MLFLOW? can"t connect, that address might be incorrect')


def get_model_latest(name, stage):
    end_point = '/api/2.0/preview/mlflow/registered-models/get-latest-versions'
    host = os.environ.get('MLFLOW_TRACKING_URI', None)
    if host is None :
        raise MlflowException('MLFLOW_TRACKING_URI is not provided')
    
    uri = host + end_point
    # get all stage from model
    params = {'name' : name, 'stages' : [stage]}
    response = requests.get(uri, params=params)

    if response.status_code != 200 :
        data = response.json()
        raise MlflowException(data['error_code'])

    data = response.json()
    all_model = data.get('model_versions', None)
    if all_model is None :
        raise MlflowException('There is no model')

    return all_model[0]


def get_model_version(name, version):
    end_point = '/api/2.0/preview/mlflow/model-versions/get'
    uri = HOST + end_point
    # get all stage from model
    params = {'name' : name, 'version' : version}
    response = requests.get(uri, params=params)
    data = response.json()
    if data.get('error_code', None) is not None :
        return None
    elif response.status_code == 200 :
        return data['model_version']
    else :
        raise MlflowException('Oops, Cannot get the model, something wrong')


def transit_latest_model_stage(name, stage_from, stage_to):
    model = get_model_latest(name, stage_from)
    client.transition_model_version_stage(
        name=name, version=model['version'], stage=stage_to
    )


def log_model(flavour_model, artifact_path, registered_model_name=None, as_production=False, await_registration=5*60, **kwargs):
    # store model
    with TempDir() as tmp:
        local_path = tmp.path('model')
        run_id = mlflow.tracking.fluent._get_or_start_run().info.run_id
        mlflow.pyfunc.save_model(path=local_path, python_model=flavour_model, **kwargs)
        mlflow.tracking.fluent.log_artifacts(local_path, artifact_path)
    
    # register model
    if registered_model_name is not None :
        registered_model = mlflow.register_model(
                    "runs:/%s/%s" % (run_id, artifact_path),
                    registered_model_name,
                    await_registration_for=await_registration
                )
        
        # model as production
        if as_production :
            # transit all production model from particular name to archive
            transit_latest_model_stage(registered_model_name, 'Production', 'Archived')
            # transit current model to production
            client.transition_model_version_stage(
                name=registered_model_name, version=registered_model.version, stage='Production'
            )


def log_built_in_flavor_model(flavor_name:str, model, artifact_path, registered_model_name, curr_production_model=None):
    getattr(mlflow, flavor_name).log_model(model, artifact_path)

    run_id = mlflow.tracking.fluent._get_or_start_run().info.run_id
    registered_model = mlflow.register_model(
                "runs:/%s/%s" % (run_id, artifact_path),
                registered_model_name,
                await_registration_for=300
            )

    if curr_production_model is not None :
        try :
            transit_latest_model_stage(registered_model_name, 'Production', 'Archived')
        except Exception as e :
            if str(e) == 'There is no model':
                pass
            else :
                raise Exception('Fail to archiving current production model')
    client.transition_model_version_stage(
        name=registered_model_name, version = registered_model.version, stage='Production'
    )


def take_step_model_version(name, curr_version, method):
    if method == 'rollback' :
        to_version = int(curr_version) - 1
        if to_version <= 0 :
            return {'model':None, 'message':'There is no previous model'}
    elif method == 'rollup' :
        latest_version = get_latest_version_of_model(name)
        to_version = int(curr_version) + 1
        if to_version > int(latest_version) :
            return {'model':None, 'message':'There is no next model'}
    else :
        raise MlflowException('Roll method is not recognized')

    to_model = get_model_version(name, to_version)
    if to_model is None :
        return take_step_model_version(name, to_version, method)
    else :
        return {'model':to_model, 'message':'New Model'}


def roll_production_model(name, method):
    current_prod_model = get_model_latest(name, 'Production')
    curr_version = current_prod_model['version']
    new_model_step = take_step_model_version(name, curr_version, method)
    new_model = new_model_step['model']
    if new_model is None :
        return new_model_step['message']
    new_version = new_model['version']
    client.transition_model_version_stage(
        name=name, version=curr_version, stage='Archived'
    )
    client.transition_model_version_stage(
        name=name, version=new_version, stage='Production'
    )
    return f'Production model has been roll from {curr_version} to {new_version}'



def get_latest_version_of_model(name):
    end_point = '/api/2.0/preview/mlflow/registered-models/get-latest-versions'
    uri = HOST + end_point
    # get all stage from model
    params = {'name' : name, 'stages' : ['Production', 'Archived', 'None']}
    response = requests.get(uri, params=params)
    data = response.json()
    all_models = data.get('model_versions', None)
    if all_models is None :
        raise MlflowException('There is no models')

    all_version = [ model['version'] for model in all_models ]
    return max(all_version)