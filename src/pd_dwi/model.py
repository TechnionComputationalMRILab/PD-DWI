from pickle import dump, load as pkl_load, HIGHEST_PROTOCOL
from typing import Optional, Callable, Union, TextIO

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from pd_dwi.config.config import ModelConfig
from pd_dwi.config.utils import read_config
from pd_dwi.dataset import create_dataset, validate_dataset
from pd_dwi.training_utils import create_model_from_config


class Model(object):
    def __init__(self, config: ModelConfig, model_obj: Optional[Union[GridSearchCV, Pipeline]] = None) -> None:
        self.config: ModelConfig = config
        self.model = model_obj

    @classmethod
    def from_config(cls, config: Union[str, TextIO]) -> 'Model':
        return cls(config=read_config(config))

    def save(self, path: str) -> None:
        assert self.model is not None

        with open(path, mode='wb') as f:
            dump(self, f, HIGHEST_PROTOCOL)

        print(f'Model saved successfully to: {path}')

    @classmethod
    def load(cls, path: str) -> 'Model':
        with open(path, mode='rb') as f:
            return pkl_load(f)

    def train(self, dataset_path: str) -> 'Model':
        assert self.config is not None

        X_train, y_train = create_dataset(dataset_path, self.config.dataset)
        validate_dataset(X_train, y_train, True)

        model = create_model_from_config(self.config)
        model.fit(X_train, y_train)

        if isinstance(model, GridSearchCV):
            self._report_cross_validation(model)

        self.model = model

        self.score(dataset_path)

        return self

    def predict(self, dataset_path: str) -> pd.Series:
        assert self.model is not None

        cfg_dataset = self.config.dataset
        X, _ = create_dataset(dataset_path, cfg_dataset)
        validate_dataset(X)

        y_pred = self.model.predict(X)
        return pd.Series(y_pred, index=X.index)

    def predict_proba(self, dataset_path: str) -> pd.Series:
        assert self.model is not None

        cfg_dataset = self.config.dataset
        X, _ = create_dataset(dataset_path, cfg_dataset)
        validate_dataset(X)

        y_pred = self.model.predict_proba(X)[:, 1]
        return pd.Series(y_pred, index=X.index)

    def score(self, dataset_path: str, f_score: Optional[Callable] = None,
              use_probability: Optional[bool] = None) -> float:
        assert self.model is not None
        assert (f_score is not None) == (use_probability is not None)

        if f_score is None:
            f_score = roc_auc_score
            use_probability = True

        cfg_dataset = self.config.dataset
        X, y = create_dataset(dataset_path, cfg_dataset)

        if use_probability:
            y_pred = self.model.predict_proba(X)[:, 1]
        else:
            y_pred = self.model.predict(X)

        s = f_score(y, y_pred)
        print(f'Model score: {s:.4f}')
        return s

    def _report_cross_validation(self, model: GridSearchCV) -> None:
        if not hasattr(model, 'best_params_'):
            return

        print("Best parameters set found on development set:")
        print()
        print(model.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        cv_results = model.cv_results_
        means = cv_results["mean_test_score"]
        stds = cv_results["std_test_score"]
        for mean, std, params in zip(means, stds, cv_results["params"]):
            print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        print()
