from pickle import dump, load as pkl_load, HIGHEST_PROTOCOL

import pandas as pd
from jsonschema.validators import validate
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from yaml import FullLoader, load

from pd_dwi.dataset import create_dataset, validate_dataset
from pd_dwi.training_utils import create_model_from_config


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

        print(f'Model saved successfully to: {path}')

    @classmethod
    def load(cls, path):
        with open(path, mode='rb') as f:
            return pkl_load(f)

    def train(self, dataset_path):
        assert self.config is not None

        cfg_dataset = self.config['dataset']
        X_train, y_train = create_dataset(dataset_path, cfg_dataset)
        validate_dataset(X_train, y_train, True)

        model = create_model_from_config(self.config)
        model.fit(X_train, y_train)

        if isinstance(model, GridSearchCV):
            self._report_cross_validation(model)

        self.model = model

        s = self.score(dataset_path)
        print(f'Model score: {s:.4f}')

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

    def _report_cross_validation(self, model: GridSearchCV):
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
