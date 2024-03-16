import os
from typing import cast

import pytest
from pydantic import ValidationError

from pd_dwi.config.utils import read_config


@pytest.mark.parametrize("test_data", ["valid"], indirect=["test_data"])
def test_from_config_valid(test_data):
    read_config(test_data)

    read_config(open(test_data))


@pytest.mark.parametrize(
    'test_data,validation_msg',
    [
        ('invalid_no_modalities', 'Field required'),
        ('invalid_encoders_bad_modality', 'Value error, Encoders contain modalities that are not available in dataset'),
        ('invalid_encoders_bad_time_points',
         'Value error, Encoders contain time points that are not available in dataset')
    ],
    indirect=['test_data']
)
def test_from_config_invalid(test_data, validation_msg):
    with pytest.raises(ValidationError) as e:
        read_config(test_data)
    assert cast(ValidationError, e.value).errors()[0]['msg'] == validation_msg


def test_sample_configs():
    sample_configs_folder = os.path.join(os.path.dirname(__file__), '../src/pd_dwi/config/samples')
    for filename in os.listdir(sample_configs_folder):
        read_config(os.path.join(sample_configs_folder, filename))
