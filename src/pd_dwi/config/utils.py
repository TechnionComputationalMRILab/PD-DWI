from typing import Union

from typing_extensions import TextIO
from yaml import load, FullLoader

from pd_dwi.config.config import ModelConfig


def read_config(config: Union[str, TextIO]) -> ModelConfig:
    if hasattr(config, 'read'):
        config = load(config, Loader=FullLoader)
    elif config.endswith('.yaml') or config.endswith('.yml'):
        config = load(open(config), Loader=FullLoader)
    else:
        raise NotImplementedError()

    return ModelConfig.model_validate(config)
