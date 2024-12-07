from logging import warning
import os.path
from typing import Mapping, Optional, Set

import numpy as np
from numpy import ma

from pd_dwi.dcm_utils.reader import DicomReader
from pd_dwi.dcm_utils.tags import DicomHeader
from pd_dwi.dcm_utils.writer import DicomWriter


class ADCMap(object):
    def __init__(self, b_values: Set[int]):
        assert len(b_values) >= 2, "ADC calculation requires at least 2 b-values"
        
        self._b_values = sorted(b_values)
        
    @property
    def b_values(self):
        return self._b_values
    
    def transform(self, dwi_data_folder, output_file_name: Optional[str]) -> np.ndarray:
        dwi_readers = self._load_DWI_sequences(dwi_data_folder, self._b_values)

        shape = dwi_readers[self._b_values[0]].shape
        
        if len(shape) == 3:
            adc_pixel_array = np.zeros(shape, dtype=np.float64)
            for slice_idx in range(shape[0]):
                _, slope = self._fit_slice([dwi_readers[b].pixel_array[slice_idx] for b in self._b_values])
                adc_pixel_array[slice_idx] = slope
        elif len(shape) == 2:
            _, adc_pixel_array = self._fit_slice([dwi_readers[b].pixel_array for b in self._b_values])

        if output_file_name:
            self.write(adc_pixel_array, output_file_name, dwi_readers[self._b_values[0]])
        
        return adc_pixel_array
    
    def write(self, pixel_array, output_file_name, metadata_reference_reader):
        description = "ADC from bVals=" + ','.join(map(str, self._b_values))
        
        output_file_path = output_file_name
        
        with DicomWriter(output_file_path) as writer:
            writer.image(pixel_array, multiply_by=1000)
            writer.metadata_like(metadata_reference_reader)
            writer.image_type(['DERIVED', 'PRIMARY', 'DIFFUSION', 'ADC'])
            writer.series_description(description)
            writer.comment('Created using Least-Squares Line Fit (matrices implementation)')

    
    def _fit_slice(self, dwi_observations):
        """ Calculates linear line fit for a given slice """

        num_rows, num_columns = dwi_observations[0].shape
        num_dwi_images = len(self._b_values)
        num_pixels = num_rows * num_columns

        # variables are all non 0 b value
        variables = -np.array(self._b_values[1:])
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

    @staticmethod
    def _load_DWI_sequences(dwi_data_folder: str, b_values: Set[int]) -> Mapping[str, DicomReader]:
        def _create_and_validate(b):
            reader = DicomReader(os.path.join(dwi_data_folder, f'DWI-{b}.dcm'))
                                
            if reader.HasMetaDataKey(DicomHeader.b_value):
                assert int(reader.GetMetaData(DicomHeader.b_value)) == b
            else:
                warning(f'{DicomHeader.b_value} was not found in Dicom header')
                
            return reader
        
        return dict(map(lambda b: (b, _create_and_validate(b), b_values)))
    

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
