import argparse
import os
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
from jsonschema.validators import validate
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier
from yaml import load, FullLoader

from pd_dwi.feature_selection.select_k_best import SelectKBest
from pd_dwi.preprocessing.column_transformer import ColumnTransformer
from pd_dwi.preprocessing.transformers.hormone_receptor_encoder import HormoneReceptorEncoder
from pd_dwi.preprocessing.transformers.radiomics_encoder import RadiomicsEncoder
from pd_dwi.preprocessing.transformers.sbr_grade_encoder import SBRGradeEncoder


def create_dataset(dataset_root: str, cfg_dataset, require_labels: bool=True):
    time_points = cfg_dataset['time_points']

    df_clinical_data = pd.read_csv(os.path.join(dataset_root, 'clinical.csv'), index_col='Patient ID DICOM')\
        .replace({np.nan: None})

    subjects = {}
    for subject_folder_name in os.listdir(dataset_root):
        if subject_folder_name == 'ACRIN-6698-688291':
            continue

        subject_path = os.path.join(dataset_root, subject_folder_name)
        if not Path(subject_path).is_dir():
            continue

        subjects[subject_folder_name] = {}

        subject_clinical_data = df_clinical_data.loc[subject_folder_name]
        label = subject_clinical_data['pcr']
        if label not in [cfg_dataset['labels']['negative'], cfg_dataset['labels']['positive'], None]:
            raise ValueError(f"Label {label} is not supported. Please use 'pCR' and 'Non-pCR' values.")

        if require_labels and label is None:
            raise FileNotFoundError(f'Could not locate label.txt for {subject_folder_name}, '
                                    f'use require_labels=False if labels are not required.')

        subjects[subject_folder_name]['label'] = label

        for clinical_col in ['hrher4g', 'SBRgrade', 'race', 'Ltype']:
            subjects[subject_folder_name][clinical_col] = subject_clinical_data[clinical_col]

        for tp in time_points:
            tp_path = os.path.join(subject_path, tp)
            if not os.path.exists:
                raise FileNotFoundError(f'Could not find {tp} for {subject_folder_name}.')

            for image_name in cfg_dataset['modalities'] + [cfg_dataset['mask']]:
                file_path = os.path.join(tp_path, f'{image_name}.dcm')
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f'{image_name}.dcm is missing for {subject_folder_name} at {tp}')
                subjects[subject_folder_name][f"{tp}_{image_name.replace(' ', '_')}"] = file_path

    df = pd.DataFrame.from_dict(subjects, orient='index')

    X = df.drop(columns='label')
    y = df['label'].replace({cfg_dataset['labels']['negative']: 0, cfg_dataset['labels']['positive']: 1})
    return X, y


def create_pipeline_from_config(cfg, y_train):
    radiomic_transformers = []
    cfg_radiomics = cfg['training']['features_transformer']['radiomics']
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

    features_selection = SelectKBest(f_classif, k=cfg['training']['feature_selection']['k'])

    scale_pos_weight = cfg['training']['classifier']['scale_pos_weight']
    if scale_pos_weight == 'balanced':
        cfg['training']['classifier']['scale_pos_weight'] = np.sum(y_train == 0) / np.sum(y_train == 1)
    classifier = XGBClassifier(
        random_state=42,
        use_label_encoder=False,
        # training
        **cfg['training']['classifier']
    )

    pipeline = Pipeline(
        steps=[
            ('features_transformer', features_transformer),
            ('features_selection', features_selection),
            ('classifier', classifier)
        ]
    )
    return pipeline


def train_model(train_dataset_path, test_dataset, config):
    c = load(config, Loader=FullLoader)
    validate(instance=c, schema=load(open('./configurations/schema.yaml'), Loader=FullLoader))
    # TODO: add validation of radiomics schema

    X_train, y_train = create_dataset(train_dataset_path, c['dataset'])
    X_test, y_test = create_dataset(test_dataset, c['dataset'], c['dataset']['labels']['require_test_labels'])

    pipeline = create_pipeline_from_config(c, y_train)
    pipeline.fit(X_train, y_train)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train_dataset', type=str)
    parser.add_argument('test_dataset', type=str)
    parser.add_argument('-config', type=open)

    args = parser.parse_args()

    train_model(args.train_dataset, args.test_dataset, args.config)