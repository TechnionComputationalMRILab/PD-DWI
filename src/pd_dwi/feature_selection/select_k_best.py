import pandas as pd
from sklearn.feature_selection import SelectKBest as SelectKBestBase


class SelectKBest(SelectKBestBase):
    """
    Extension of sklearn.feature_selection.SelectKBest which returns the dataset as a pd.DataFrame
    and preserves readable feature names
    """
    def transform(self, X):
        array = super(SelectKBest, self).transform(X)
        return pd.DataFrame(array, index=X.index, columns=self.get_feature_names_out(self.feature_names_in_))