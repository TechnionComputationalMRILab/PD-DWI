import os.path
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, MagicMock

import numpy as np
from pydicom import FileDataset, DataElement

from pd_dwi.preprocessing.adc import calculate_adc_slice, calculate_adc


def test_adc_fit():
    slice_shape = (2, 2)
    b_vector = (0, 100, 200, 400)

    syntehtic_s0 = np.array(np.random.randint(500, 2000, slice_shape), dtype=np.float64)
    syntentic_adc = np.random.randint(1, 10, slice_shape) / 1000

    S = np.stack([syntehtic_s0] + [_adc_formula(syntehtic_s0, syntentic_adc, b) for b in b_vector[1:]])
    assert S.shape == (len(b_vector),) + slice_shape

    out_S0, out_ADC = calculate_adc_slice(b_vector, S)

    assert np.all(np.isclose(out_S0, syntehtic_s0))
    assert np.all(np.isclose(out_ADC, syntentic_adc))


def test_calculate_adc(mocker):
    volume_shape = (100, 2, 2)

    b_values = {0, 100, 500}

    with TemporaryDirectory() as temp_dir:
        b_value_files = [os.path.join(temp_dir, f'DWI-{b}.dcm') for b in b_values]

        mocker.patch('pd_dwi.preprocessing.adc._find_dwi_files', return_value=b_value_files)

        def dcm_mock(path):
            mock = MagicMock(spec=FileDataset)
            mock.pixel_array = np.array(np.random.randint(500, 2000, volume_shape), dtype=np.float64)
            mock.filename = Path(path).name
            return mock

        def b_value_mock(dcm):
            return int(dcm.filename.split('-')[1].replace('.dcm', ''))

        mocker.patch('pd_dwi.preprocessing.adc.dcmread', side_effect=dcm_mock)
        mocker.patch('pd_dwi.preprocessing.adc.read_b_value', side_effect=b_value_mock)

        calculate_adc(temp_dir, b_values=b_values)


def _adc_formula(s0, adc_model, b_value):
    return s0 * np.exp(-b_value * adc_model)