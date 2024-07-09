import os.path
from operator import itemgetter
from pathlib import Path
from typing import Set, List, Optional

import numpy as np
from SimpleITK import GetImageFromArray, WriteImage
from numpy import ma
from pydicom import dcmread

from pd_dwi.utils.dcm_utils import create_file_reader, copy_metadata_from_image_series_reader, read_b_value


def _find_dwi_files(dwi_input_folder: str, b_values: Set[int]) -> List[str]:
    dwi_file_paths: List[str] = []

    for b_value in b_values:
        b_value_path = os.path.join(dwi_input_folder, f'DWI-{b_value}.dcm')

        if not os.path.exists(b_value_path):
            raise ValueError(f"B-value `{b_value}` is not available in `{dwi_input_folder}.")

        dcm = dcmread(b_value_path, stop_before_pixels=True)
        b_value_value = read_b_value(dcm)
        assert b_value == b_value_value
        dwi_file_paths.append(b_value_path)

    return dwi_file_paths


def _least_squares_line_fit(variables: np.array, observations: np.array):
    """
    Fits linear line for each of set of observations

    :param variables: Explanatory variables, shared by all sets of observations
    :param observations: At least one set of observations.
                         Each column in matrix represents a set of observations that should be fitted.
    :return: intercept and slope vectors
    """

    Y = observations

    # Add column of ones to the explanatory variables
    X = np.stack((np.ones(variables.shape[0]), variables), axis=1)
    assert X.shape == (variables.shape[0], variables.shape[1] if variables.ndim == 2 else 2)

    x = np.linalg.lstsq(X, Y, rcond=None)

    intercept = np.exp(x[0][0])
    slope = x[0][1]
    return intercept, slope


def calculate_adc_slice(b_values, dwi_observations):
    """ Calculates linear line fit for a given slice """

    num_rows, num_columns = dwi_observations[0].shape
    num_dwi_images = len(b_values)
    num_pixels = num_rows * num_columns

    # variables are all non 0 b value
    variables = -np.array(b_values[1:])
    assert variables.shape == (num_dwi_images - 1,)

    # observations are from non 0 b value
    observations = np.stack([ma.log(img.flatten()).filled(0)
                             for img in dwi_observations[1:]], axis=0)
    assert observations.shape == (num_dwi_images - 1, num_pixels)

    intercept, slope = _least_squares_line_fit(variables, observations)
    assert slope.shape == (num_pixels,)

    intercept = intercept.reshape((num_rows, num_columns))
    slope = slope.reshape((num_rows, num_columns))

    # Keep only positive slopes
    slope = np.clip(slope, 0, None)

    return intercept, slope


def _save_adc(adc_data: np.ndarray, b_values: Set[int], dwi_ref_file_path: str, output_folder: str,
              comments: Optional[str] = None):
    reader = create_file_reader(dwi_ref_file_path)
    ref_dwi_image = reader.Execute()

    adc_image = GetImageFromArray(adc_data * 1000)
    adc_image.SetSpacing(ref_dwi_image.GetSpacing())
    adc_image.SetDirection(ref_dwi_image.GetDirection())
    adc_image.SetOrigin(ref_dwi_image.GetOrigin())

    copy_metadata_from_image_series_reader(reader, adc_image, ["0020|000e", "0020|0011", "0008|0008"])

    # Image Type
    adc_image.SetMetaData("0008|0008", reader.GetMetaData("0008|0008").replace('TRACE', 'ADC'))

    # Series Number - created by removing b_value from DWI series number and 0100
    b_value = int(reader.GetMetaData("0018|9087"))
    base_series_number = reader.GetMetaData("0020|0011")[:-len(f'{b_value:03d}') + 4]
    adc_image.SetMetaData("0020|0011", f'{base_series_number}0200')

    # Rescale intercept
    adc_image.SetMetaData("0028|1052", "0")
    # Rescale Slope
    adc_image.SetMetaData("0028|1053", "0.001")
    # Rescale Type
    adc_image.SetMetaData("0028|1054", "10^-3mm^2/s ")

    # Series description
    b_values_str = ','.join([str(b) for b in b_values])
    description = f"ADC from bVals={b_values_str}"
    adc_image.SetMetaData("0008|103e", description)

    if comments:
        adc_image.SetMetaData("0020|4000", comments)

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    WriteImage(adc_image, os.path.join(output_folder, f"{description}.dcm"))


def calculate_adc_from_files(*dwi_file_paths) -> np.ndarray:
    """
    Calculates ADC data from list of DWI files

    :param dwi_file_paths: DWI acquisition file paths, representing the b-values to use in ADC calculation

    :return: ADC data
    """

    if len(dwi_file_paths) < 2:
        raise ValueError("At least two DWI sequences should be provided")

    dwi_observations = []

    for dwi_path in dwi_file_paths:
        dcm = dcmread(dwi_path)
        dwi_observations.append((read_b_value(dcm), dcm.pixel_array))

    dwi_observations = sorted(dwi_observations, key=lambda x: x[0])
    b_values, dwi_arrays = zip(*dwi_observations)

    adc_shape = dwi_arrays[0].shape
    adc_data = np.zeros(adc_shape, dtype=np.float64)
    for slice_idx in range(adc_shape[0]):
        _, slope = calculate_adc_slice(b_values, list(map(itemgetter(slice_idx), dwi_arrays)))
        adc_data[slice_idx] = slope

    return adc_data


def calculate_adc(dwi_input_folder: str, b_values: Set[int], output_folder: Optional[str] = None) -> np.ndarray:
    """
    Calculates ADC data from DWI acquisition and set of input b-values

    :param dwi_input_folder: Path of DWI acquisition folder
    :param b_values: Unique array of b-values to use in ADC calculation
    :param output_folder: Path of output folder to store calculated ADC in

    :return: ADC data
    """
    dwi_file_paths = _find_dwi_files(dwi_input_folder, b_values)
    adc_data = calculate_adc_from_files(*dwi_file_paths)

    if output_folder:
        _save_adc(adc_data, b_values, dwi_file_paths[0], output_folder,
                  comments="Created using Least-Squares Line Fit (matrices implementation)")

    return adc_data
