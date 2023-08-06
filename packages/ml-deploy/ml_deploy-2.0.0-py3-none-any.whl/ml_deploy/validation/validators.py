from ml_deploy.validation.config import (
    AppConfig, DataConfig, ModelConfig, AllConfig,
    ModelParamsConfig, ModelPerformanceConfig, AllConfig
    )
from ml_deploy.validation.utils import is_file_exists

from strictyaml import load


def fetch_config_from_yaml(cfg_path:str) -> dict:
    """Parse YAML containing the package configuration."""
    print(cfg_path)
    if not is_file_exists(cfg_path):
        raise OSError(f"File not found at {cfg_path!r}")
        

    with open(cfg_path, "r") as conf_file:
        parsed_config = load(conf_file.read())
        return parsed_config.data


def create_and_validate_config(cfg_path:str=None):
    if cfg_path is None:
        _config = AllConfig()
    else :
        yaml_config = fetch_config_from_yaml(cfg_path)
        _config = AllConfig(**yaml_config)
    return _config