import logging
import os
import warnings
from multiprocessing import Pool

import numpy as np
import pandas as pd
from numpy import ndarray
from radiomics import getFeatureClasses, setVerbosity
from radiomics.featureextractor import RadiomicsFeatureExtractor
from sklearn.base import BaseEstimator, TransformerMixin

setVerbosity(logging.ERROR)

RADIOMICS_ENCODER_CORES = int(os.getenv('RE_JOBS', 1))


class RadiomicsEncoder(TransformerMixin, BaseEstimator):
    """
    Extracts radiomic features from input image according to tumour mask
    """
    def __init__(self, image, mask, cfg_radiomics=None):
        self.image = image
        self.mask = mask
        self.radiomics_extractor = None
        self.radiomics_ = None
        self.cfg_radiomics = cfg_radiomics
        self.num_workers = cfg_radiomics.get('workers')
        self.setup_radiomics_extractor(cfg_radiomics)

    def setup_radiomics_extractor(self, cfg_radiomics):
        if cfg_radiomics is None:
            cfg_radiomics = dict()

        settings = cfg_radiomics.get('setting', {})
        settings['additionalInfo'] = False

        supported_feature_classes = getFeatureClasses().keys()
        if 'featureClass' in cfg_radiomics:
            feature_class_names = set(cfg_radiomics['featureClass'].keys())

            if 'shape2D' in feature_class_names and not settings.get('force2D', False):
                raise ValueError('shape2D cannot be used without force2D')

            if not feature_class_names.issubset(supported_feature_classes):
                raise ValueError('input features are not recognized by pyradiomics.')
        else:
            cfg_radiomics['featureClass'] = {}
            for fc in supported_feature_classes:
                if fc == 'shape2D':
                    continue

                cfg_radiomics['featureClass'][fc] = []

        self.radiomics_extractor = RadiomicsFeatureExtractor(cfg_radiomics)

    def fit(self, X, y=None):
        transformed = self.transform(X[:1])
        self.radiomics_ = list(transformed.columns)

        return self

    def transform(self, X: pd.DataFrame):
        assert isinstance(X, pd.DataFrame), 'Input data must be pd.DataFrame'

        if (RADIOMICS_ENCODER_CORES > 1) and len(X) > RADIOMICS_ENCODER_CORES:
            X_transformed = self._parallel_transform(X)
        else:
            X_transformed = self._serial_transform(X)

        return X_transformed.replace({np.inf: 1, np.nan: 1})

    def get_feature_names(self, input_features=None):
        return self.radiomics_

    def get_feature_names_out(self, input_features=None):
        return self.radiomics_

    def _transform_sample(self, row):
        features_vector = self.radiomics_extractor.execute(row[self.image], row[self.mask])
        for key, value in features_vector.items():
            if isinstance(value, float) or isinstance(value, int):
                features_vector[key] = value
            elif isinstance(value, ndarray) and value.size == 1:
                features_vector[key] = value.item()
            else:
                warnings.warn(f"Feature {key} is not numeric, replacing with null", UserWarning)
                features_vector[key] = None

        return pd.Series(features_vector)

    def _serial_transform(self, X):
        return X.apply(self._transform_sample, axis=1)

    def _parallel_transform(self, X):
        X_split = np.array_split(X, RADIOMICS_ENCODER_CORES)
        pool = Pool(RADIOMICS_ENCODER_CORES)
        X_transformed = pd.concat(pool.map(self._serial_transform, X_split))
        pool.close()
        pool.join()
        return X_transformed
