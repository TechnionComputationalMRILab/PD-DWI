import os
from pathlib import Path

import numpy as np
import pandas as pd


def create_dataset(dataset_root: str, cfg_dataset):
    df_clinical_data = pd.read_csv(os.path.join(dataset_root, 'clinical.csv'), index_col='Patient ID DICOM') \
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

        subjects[subject_folder_name]['label'] = label

        for clinical_col in ['hrher4g', 'SBRgrade', 'race', 'Ltype']:
            subjects[subject_folder_name][clinical_col] = subject_clinical_data[clinical_col]

        for tp in cfg_dataset['time_points']:
            tp_path = os.path.join(subject_path, tp)
            if not os.path.exists:
                raise FileNotFoundError(f'Could not find {tp} [subject: {subject_folder_name}].')

            for image_name in cfg_dataset['modalities'] + cfg_dataset['masks']:
                file_path = os.path.join(tp_path, f'{image_name}.dcm')
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f'{image_name}.dcm is not found [subject: {subject_folder_name}]')
                subjects[subject_folder_name][f"{tp} {image_name}"] = file_path

    df = pd.DataFrame.from_dict(subjects, orient='index')

    X = df.drop(columns='label')
    y = df['label'].replace({cfg_dataset['labels']['negative']: 0, cfg_dataset['labels']['positive']: 1})
    return X, y


def validate_dataset(X: pd.DataFrame, y: pd.Series = None, require_label=False):
    """ Validates dataset according to expected structure """

    if not isinstance(X, pd.DataFrame):
        raise ValueError('X must be instance of pd.DataFrame')

    if not require_label:
        return

    if not isinstance(y, pd.Series):
        raise ValueError('y must be instance of pd.Series')

    if require_label:
        if np.sum(y.isnull()) > 0:
            raise ValueError('All subjects in dataset must have a label')

        if not set(y.unique()).issubset([0, 1]):
            raise ValueError('Labels must be 0 or 1')
