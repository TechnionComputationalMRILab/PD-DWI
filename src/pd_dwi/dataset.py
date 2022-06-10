import os
from pathlib import Path

import numpy as np
import pandas as pd


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
            raise ValueError(f"Label {label} is not supported  [subject: {subject_folder_name}]. "
                             f"Please use 'pCR' and 'Non-pCR' values.")

        if require_labels and label is None:
            raise ValueError(f'Label is unknown [subject: {subject_folder_name}].')

        subjects[subject_folder_name]['label'] = label

        for clinical_col in ['hrher4g', 'SBRgrade', 'race', 'Ltype']:
            subjects[subject_folder_name][clinical_col] = subject_clinical_data[clinical_col]

        for tp in time_points:
            tp_path = os.path.join(subject_path, tp)
            if not os.path.exists:
                raise FileNotFoundError(f'Could not find {tp} [subject: {subject_folder_name}].')

            for image_name in cfg_dataset['modalities'] + [cfg_dataset['mask']]:
                file_path = os.path.join(tp_path, f'{image_name}.dcm')
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f'{image_name}.dcm is not found [subject: {subject_folder_name}]')
                subjects[subject_folder_name][f"{tp}_{image_name.replace(' ', '_')}"] = file_path

    df = pd.DataFrame.from_dict(subjects, orient='index')

    X = df.drop(columns='label')
    y = df['label'].replace({cfg_dataset['labels']['negative']: 0, cfg_dataset['labels']['positive']: 1})
    return X, y
