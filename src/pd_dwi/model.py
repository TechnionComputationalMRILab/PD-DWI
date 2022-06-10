from itertools import product
from pickle import dump, load as pkl_load, HIGHEST_PROTOCOL

import numpy as np
import pandas as pd
from jsonschema.validators import validate
from sklearn.feature_selection import f_classif
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier
from yaml import FullLoader, load

from pd_dwi.dataset import create_dataset, validate_dataset
from pd_dwi.feature_selection.select_k_best import SelectKBest
from pd_dwi.preprocessing.column_transformer import ColumnTransformer
from pd_dwi.preprocessing.transformers.hormone_receptor_encoder import HormoneReceptorEncoder
from pd_dwi.preprocessing.transformers.radiomics_encoder import RadiomicsEncoder
from pd_dwi.preprocessing.transformers.sbr_grade_encoder import SBRGradeEncoder


def create_pipeline_from_config(cfg, balanced_scale_pos_weight):
    radiomic_transformers = []
    cfg_radiomics = cfg['pipeline']['features_transformer'].get('radiomics')
    for tp, modality in product(cfg['dataset']['time_points'], cfg['dataset']['modalities']):
        modality_col_name = f"{tp}_{modality}".replace(' ', '_')
        mask_col_name = f"{tp}_{cfg['dataset']['mask']}".replace(' ', '_')
        radiomic_transformers.append((modality_col_name,
                                      RadiomicsEncoder(modality_col_name, mask_col_name, cfg_radiomics),
                                      [modality_col_name, mask_col_name]))

    clinical_transformers = [
        ('hrher', HormoneReceptorEncoder(), ['hrher4g']),
        ('sbrgrade', SBRGradeEncoder(), ['SBRgrade']),
        ('cat', OneHotEncoder(handle_unknown="ignore"), ['race', 'Ltype'])
    ]

    features_transformer = ColumnTransformer(
        transformers=radiomic_transformers + clinical_transformers,
        remainder='drop'
    )

    cfg_feature_selection = cfg['pipeline'].get('feature_selection')
    if cfg_feature_selection is None:
        features_selection = SelectKBest(f_classif)
    else:
        features_selection = SelectKBest(f_classif, k=cfg_feature_selection['k'])

    cfg_classifier = cfg['pipeline'].get('classifier', {})
    scale_pos_weight_value = cfg_classifier.get('scale_pos_weight')
    if scale_pos_weight_value == 'balanced':
        cfg_classifier['scale_pos_weight'] = balanced_scale_pos_weight

    classifier = XGBClassifier(
        random_state=42,
        use_label_encoder=False,
        validate_parameters=True,
        **cfg_classifier
    )

    pipeline = Pipeline(
        steps=[
            ('features_transformer', features_transformer),
            ('features_selection', features_selection),
            ('classifier', classifier)
        ]
    )

    return pipeline


def create_model_from_config(cfg, balanced_scale_pos_weight):
    pipeline = create_pipeline_from_config(cfg, balanced_scale_pos_weight)

    cfg_grid_search_cv = cfg.get('grid_search_cv')
    if cfg_grid_search_cv is None:
        return pipeline

    param_grid = {}
    for step_name, step_parameters in cfg_grid_search_cv['param_grid'].items():
        for parameter_name, values in step_parameters.items():
            if step_name == 'classifier' and parameter_name == 'scale_pos_weight':
                if 'balanced' in values:
                    values.remove('balanced')
                    values.append(balanced_scale_pos_weight)

            param_grid[f'{step_name}__{parameter_name}'] = values

    del cfg_grid_search_cv['param_grid']

    return GridSearchCV(pipeline, param_grid, **cfg_grid_search_cv)


class Model(object):
    def __init__(self, config=None, model_obj=None):
        self.config = config
        self.model = model_obj

    @classmethod
    def from_config(cls, config):
        if hasattr(config, 'read'):
            config = load(config, Loader=FullLoader)
        elif not isinstance(config, dict):
            raise NotImplementedError()

        validate(instance=config, schema=load(open('./configurations/schema.yaml'), Loader=FullLoader))

        return cls(config=config)

    def save(self, path):
        assert self.model is not None

        with open(path, mode='wb') as f:
            dump(self, f, HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path):
        with open(path, mode='rb') as f:
            return pkl_load(f)

    def train(self, dataset_path):
        assert self.config is not None

        cfg_dataset = self.config['dataset']
        X_train, y_train = create_dataset(dataset_path, cfg_dataset)
        validate_dataset(X_train, y_train, True)
        balanced_scale_pos_weight = np.sum(y_train == 0) / np.sum(y_train == 1)

        model = create_model_from_config(self.config, balanced_scale_pos_weight)
        model.fit(X_train, y_train)

        self.model = model

        return self

    def predict(self, dataset_path):
        assert self.model is not None

        cfg_dataset = self.config['dataset']
        X, _ = create_dataset(dataset_path, cfg_dataset)
        validate_dataset(X)

        y_pred = self.model.predict(X)
        return pd.Series(y_pred, index=X.index)

    def predict_proba(self, dataset_path):
        assert self.model is not None

        cfg_dataset = self.config['dataset']
        X, _ = create_dataset(dataset_path, cfg_dataset)
        validate_dataset(X)

        y_pred = self.model.predict_proba(X)[:, 1]
        return pd.Series(y_pred, index=X.index)

    def score(self, dataset_path, f_score=None, use_probability=None):
        assert self.model is not None
        assert (f_score is not None) == (use_probability is not None)

        if f_score is None:
            f_score = roc_auc_score
            use_probability = True

        cfg_dataset = self.config['dataset']
        X, y = create_dataset(dataset_path, cfg_dataset)

        if use_probability:
            y_pred = self.model.predict_proba(X)[:, 1]
        else:
            y_pred = self.model.predict(X)

        return f_score(y, y_pred)

