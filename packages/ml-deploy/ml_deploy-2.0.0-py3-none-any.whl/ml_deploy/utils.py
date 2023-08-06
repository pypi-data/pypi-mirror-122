from ml_deploy.validation.validators import create_and_validate_config
import importlib
import os, sys
import argparse
sys.path.append(os.getcwd())


def load_class(interface_name):
    
    parts = interface_name.rsplit(".", 1)
    if len(parts) == 1: # if class name is the same with file name
        interface_file = importlib.import_module(interface_name)
        user_class = getattr(interface_file, interface_name)
    else: # if class name is different with file name
        interface_file = importlib.import_module(parts[0])
        user_class = getattr(interface_file, parts[1])

    return user_class


def bool_as_str(val):
    if not isinstance(val, bool):
        return val.lower() in ["1", "true", "t"]
    return val


def bool_env_var(*env_vars, default=False):
    """Convert boolean value as string data type to boolean data type"""
    val = getenv(*env_vars)

    if val is None :
        return default

    return bool_as_str(val)


def getenv(*env_vars, default=None):
    """
    Overload of os.getenv() to allow falling back through multiple environment
    variables. The environment variables will be checked sequentially until one
    of them is found.
    Parameters
    ------
    *env_vars
        Variadic list of environment variable names to check.
    default
        Default value to return if none of the environment variables exist.
    Returns
    ------
        Value of the first environment variable set or default.
    """
    for env_var in env_vars:
        if env_var in os.environ:
            return os.environ.get(env_var)

    return default


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--config',
        type=str,
        help='Application config',
        default='config.yaml'
    )

    args, _ = parser.parse_known_args()
    pipeline_config = create_and_validate_config(args.config)
    app_config = pipeline_config.app
    del pipeline_config.app
    parser.add_argument(
        "--interface-name", 
        type=str, 
        default=app_config.interface,
        help="Name of the user interface.")

    parser.add_argument("--metric-class", type=str, default=app_config.metric_class)
    
    parser.add_argument(
        "--http-port",
        type=int,
        default=app_config.http_port,
        help="Http port for flask REST API"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default=app_config.mode,
        help="App environment",
    )

    parser.add_argument(
        "--app-debug",
        nargs="?",
        type=str,
        default=app_config.debug,
        const=True,
        help="Enable debug mode.",
    )

    parser.add_argument(
        "--kafka-broker",
        type=str,
        default=app_config.kafka_broker,
        help="Connect to kafka broker.",
    )

    # Gunicorn Settings
    parser.add_argument(
        "--gunicorn-access-log",
        nargs="?",
        type=str,
        default=os.environ.get('GUNICORN_ACCESS_LOG', 'false'),
        const=True,
        help="Enable gunicorn access log.",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=app_config.log_level,
        help="Log level of the inference server.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=app_config.workers,
        help="Number of Gunicorn workers for handling requests.",
    )

    parser.add_argument(
        "--worker-class",
        type=str,
        default=app_config.worker_class,
        help="Gunicorn worker type."
    )

    parser.add_argument(
        "--gunicorn-timeout",
        type=int,
        default=app_config.gunicorn_timeout,
        help="Number of threads to run per Gunicorn worker.",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=app_config.threads,
        help="Number of threads to run per Gunicorn worker.",
    )

    
    parser.add_argument(
        "--max-requests",
        type=int,
        default=app_config.max_requests,
        help="Maximum number of requests gunicorn worker will process before restarting.",
    )

    parser.add_argument(
        "--max-requests-jitter",
        type=int,
        default=app_config.max_requests_jitter,
        help="Maximum random jitter to add to max-requests.",
    )

    parser.add_argument(
        "--keepalive",
        type=int,
        default=app_config.keepalive,
        help="The number of seconds to wait for requests on a Keep-Alive connection.",
    )


    parser.add_argument(
        "--single-threaded",
        type=int,
        default=int(os.environ.get("FLASK_SINGLE_THREADED", "0")),
        help="Force the Flask app to run single-threaded. Also applies to Gunicorn.",
    )

    parser.add_argument(
        "--pidfile", type=str, default=None, help="A file path to use for the PID file"
    )
    

    app_config, _ = parser.parse_known_args()
    return app_config, pipeline_config