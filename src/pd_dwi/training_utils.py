from importlib import import_module
from itertools import product

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from pd_dwi.feature_selection.select_k_best import SelectKBest
from sklearn.feature_selection import f_classif

from pd_dwi.preprocessing.column_transformer import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from pd_dwi.preprocessing.transformers.sbr_grade_encoder import SBRGradeEncoder

from pd_dwi.preprocessing.transformers.hormone_receptor_encoder import HormoneReceptorEncoder

from pd_dwi.preprocessing.transformers.radiomics_encoder import RadiomicsEncoder


def load_from_class_string(class_str):
    """ Loads class from class string """
    try:
        module_path, class_name = class_str.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(class_str)


def create_pipeline_from_config(cfg):
    radiomic_transformers = []
    cfg_radiomics = cfg['pipeline']['features_transformer'].get('radiomics')
    if cfg_radiomics:
        for modality in cfg_radiomics['encoders']:
            image_name = modality['image']
            mask_name = modality['mask']

            for time_point in modality['time_points']:
                image_col_name = f'{time_point} {image_name}'
                mask_col_name = f'{time_point} {mask_name}'
                encoder_name = image_col_name.replace(' ', '_')
                radiomic_transformers.append((encoder_name,
                                              RadiomicsEncoder(image_col_name, mask_col_name, cfg_radiomics.get('engine')),
                                              [image_col_name, mask_col_name]))

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

    cfg_classifier = cfg['pipeline']['classifier']

    classifier = load_from_class_string(cfg_classifier['module'])(**cfg_classifier.get('parameters', {}))

    pipeline = Pipeline(
        steps=[
            ('features_transformer', features_transformer),
            ('features_selection', features_selection),
            ('classifier', classifier)
        ]
    )

    return pipeline


def create_model_from_config(cfg):
    pipeline = create_pipeline_from_config(cfg)

    cfg_grid_search_cv = cfg.get('grid_search_cv')
    if cfg_grid_search_cv is None:
        return pipeline

    param_grid = {}
    for step_name, step_parameters in cfg_grid_search_cv['param_grid'].items():
        for parameter_name, values in step_parameters.items():
            param_grid[f'{step_name}__{parameter_name}'] = values

    del cfg_grid_search_cv['param_grid']

    return GridSearchCV(pipeline, param_grid, **cfg_grid_search_cv)
