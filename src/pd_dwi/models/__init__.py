from json import loads
from typing import List, Dict, Optional

from importlib_resources import files


def get_available_models() -> Dict[str, Dict[str, str]]:
    data_text = files('pd_dwi.models').joinpath('registry.json').read_text()
    available_models = loads(data_text)
    return available_models


def get_model_path_by_name(model_name: str) -> Optional[str]:
    models = get_available_models()
    if model_name not in models:
        return None

    return str(files('pd_dwi.models').joinpath(models[model_name]['filename']))
