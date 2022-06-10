from sklearn.base import TransformerMixin, BaseEstimator


class HormoneReceptorEncoder(TransformerMixin, BaseEstimator):
    """
    Splits HR/HER2 clinical data into two binary features: HR and HER2
    """
    def __init__(self):
        self.receptors_ = None

    def fit(self, X, y=None):
        transformed = self.transform(X)
        self.receptors_ = list(transformed.columns)

        return self

    def transform(self, X):
        assert 'hrher4g' in X.columns
        df = X['hrher4g'].str.split('/', expand=True).apply(lambda x: x.str.contains('+', regex=False)).astype(float)
        df.columns = ['HR', 'HER2']

        return df

    def get_feature_names(self, input_features=None):
        return self.receptors_

    def get_feature_names_out(self, input_features=None):
        return self.receptors_
