import logging
import warnings

import numpy as np
import pandas as pd
from numpy import ndarray
from radiomics import getFeatureClasses, setVerbosity
from radiomics.featureextractor import RadiomicsFeatureExtractor
from sklearn.base import BaseEstimator, TransformerMixin


class RadiomicsEncoder(TransformerMixin, BaseEstimator):
    def __init__(self, image, mask, cfg_radiomics=None):
        self.image = image
        self.mask = mask
        self.radiomics_extractor = None
        self.radiomics_ = None
        self.cfg_radiomics = cfg_radiomics
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
        setVerbosity(logging.ERROR)

    def fit(self, X, y=None):
        transformed = self.transform(X[:1])
        self.radiomics_ = list(transformed.columns)

        return self

    def transform(self, X: pd.DataFrame):
        assert isinstance(X, pd.DataFrame), 'Input data must be pd.DataFrame'

        def transform_sample(row):
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

        return X.apply(transform_sample, axis=1).replace({np.inf: 1, np.nan: 1})

    def get_feature_names(self, input_features=None):
        return self.radiomics_

    def get_feature_names_out(self, input_features=None):
        return self.radiomics_
