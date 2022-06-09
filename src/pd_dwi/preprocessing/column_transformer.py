import pandas as pd
from sklearn.compose import ColumnTransformer as ColumnTransformerBase


class ColumnTransformer(ColumnTransformerBase):
    def fit_transform(self, X, y=None):
        array = super(ColumnTransformer, self).fit_transform(X, y)
        return pd.DataFrame(array, index=X.index, columns=self.get_feature_names_out(list(X.columns)))

    def transform(self, X):
        array = super(ColumnTransformer, self).transform(X)

        return pd.DataFrame(array, index=X.index, columns=self.get_feature_names_out(list(X.columns)))