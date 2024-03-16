import tempfile

import pandas as pd
import pytest

from pd_dwi.model import Model


@pytest.mark.parametrize("test_data", ["valid"], indirect=["test_data"])
def test_save_and_load(test_data, mocker):
    X = pd.DataFrame()
    y = pd.Series()

    create_dataset_mock = mocker.patch('pd_dwi.model.create_dataset')
    create_dataset_mock.return_value = (X, y)

    xgboost_fit_mock = mocker.patch('sklearn.model_selection.GridSearchCV.fit')
    xgboost_fit_mock.return_value = None

    score_mock = mocker.patch('pd_dwi.model.Model.score')
    score_mock.return_value = None

    model = Model.from_config(test_data)
    model.train('some_fake_path')

    with tempfile.NamedTemporaryFile(suffix='.pkl', delete=True) as f:
        model.save(f.name)

        loaded_model = Model.load(f.name)
        assert loaded_model.config == model.config
