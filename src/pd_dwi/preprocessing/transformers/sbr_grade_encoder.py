import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class SBRGradeEncoder(TransformerMixin, BaseEstimator):
    """
    Transforms SBRGrade from categorical feature to ordinal feature
    """
    _ORDINAL_MAPPING = {'i (low)': 1.0, 'ii (intermediate)': 2.0, 'iii (high)': 3.0}

    def __init__(self):
        self.missing_value_ = None
        self.grade_column = 'SBRgrade'

    def fit(self, X, y=None):
        assert X.shape[1] == 1, 'Expected exactly one column'
        assert self.grade_column in X.columns, f'Expected column name: {self.grade_column}'

        # Use most common category for missing value
        self.missing_value_ = X[self.grade_column].value_counts(dropna=True, ascending=False).index[0]

        return self

    def transform(self, X, y=None):
        assert X.shape[1] == 1, 'Expected exactly one column'
        assert self.grade_column in X.columns, f'Expected column name: {self.grade_column}'

        return pd.DataFrame(X[self.grade_column].fillna(self.missing_value_).str.lower().replace(self._ORDINAL_MAPPING))

    def get_feature_names(self, input_features=None):
        return [self.grade_column]

    def get_feature_names_out(self, input_features=None):
        return [self.grade_column]
