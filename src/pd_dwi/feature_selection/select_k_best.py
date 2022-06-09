import pandas as pd
from sklearn.feature_selection import SelectKBest as SelectKBestBase


class SelectKBest(SelectKBestBase):
    def transform(self, X):
        array = super(SelectKBest, self).transform(X)
        return pd.DataFrame(array, index=X.index, columns=self.get_feature_names_out(self.feature_names_in_))