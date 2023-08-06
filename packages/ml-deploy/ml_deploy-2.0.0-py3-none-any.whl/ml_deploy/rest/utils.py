import os
from typing import List

from ml_deploy.errors import ModelMetadataError

from multiprocessing.util import _exit_function
from flask import request
import atexit


def create_response(target : dict={}, input:list=[], list_metrics:List[dict]=[],
    topics: List[str]=[]) -> dict :
    return {
        'target' : target,
        'input' : input,
        'list_metrics' : list_metrics,
        'topics' : topics
    }


def predict_request(X:list, names:List[str]=[]) -> dict:
    return {
        'X' : X,
        'names' : names
    }
    


def feedback_request(X:list, y_true:list, y_predicted:list) -> dict :
    return {
        'X' : X,
        'y_true' : y_true,
        'y_predicted' : y_predicted
    }


def check_return_model_md(user_model, arg_value, metadata):
    if arg_value not in [None, '', 'None'] :
        value_md = arg_value
    elif hasattr(user_model, metadata):
        value_md = getattr(user_model, metadata)
    else :
        raise ModelMetadataError
    
    return value_md


def process_api_prefix(api_prefix):
    replace_chars = ['_', ' ']
    for char in replace_chars:
        api_prefix = api_prefix.replace(char, "-")
    
    api_prefix = f'/{api_prefix.lower()}/api'
    return api_prefix
    

def threads(threads: int, single_threaded: bool) -> int:
    """
    Number of threads to run in each Gunicorn worker.
    """

    if single_threaded:
        return 1

    return threads


def post_worker_init(worker):
    # Remove the atexit handler set up by the parent process
    # https://github.com/benoitc/gunicorn/issues/1391#issuecomment-467010209
    atexit.unregister(_exit_function)



def cursor_rows_as_dicts(cursor):
    """convert tuple result to dict with cursor"""
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]



def get_all_request():
    """
    Get all requests data in the form of json and 
    in the content type : multipart/form-data

    All request data within multipart/form-data will be put in key 'form'
    """

    if (
        request.content_type is not None 
        and "multipart/form-data" in request.content_type
    ):
        data = get_multi_form_data_request()
    else :
        data = get_json_request()

    return data


def get_json_request():
    return request.get_json(force=True)


def get_multi_form_data_request():
    """
    Parses a request submitted with Content-type:multipart/form-data
    Get all files
    """
    form_dict = {}
    for key in request.form:
        form_dict[key] = request.form.get(key)

    for fileKey in request.files:
        form_dict[fileKey] = request.files[fileKey]

    return form_dict