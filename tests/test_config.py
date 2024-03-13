import os
from typing import cast

import pytest
from pydantic import ValidationError

from pd_dwi.config.utils import read_config

dirname = os.path.dirname(__file__)


def test_from_config_valid():
    valid_config_path = os.path.join(dirname, './data/valid.yaml')
    read_config(valid_config_path)

    read_config(open(valid_config_path))


@pytest.mark.parametrize(
    'config_name,validation_msg',
    [
        ('invalid_no_modalities', 'Field required'),
        ('invalid_encoders_bad_modality', 'Value error, Encoders contain modalities that are not available in dataset'),
        ('invalid_encoders_bad_time_points', 'Value error, Encoders contain time points that are not available in dataset')
    ]
)
def test_from_config_invalid(config_name, validation_msg):
    invalid_config_path = os.path.join(dirname, f'./data/{config_name}.yaml')
    with pytest.raises(ValidationError) as e:
        read_config(invalid_config_path)
    assert cast(ValidationError, e.value).errors()[0]['msg'] == validation_msg


def test_sample_configs():
    sample_configs_folder = os.path.join(dirname, '../src/pd_dwi/config/samples')
    for filename in os.listdir(sample_configs_folder):
        read_config(os.path.join(sample_configs_folder, filename))
