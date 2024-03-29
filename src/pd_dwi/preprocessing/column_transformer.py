from typing import Optional

import pandas as pd
from sklearn.compose import ColumnTransformer as ColumnTransformerBase


class ColumnTransformer(ColumnTransformerBase):
    """
    Extension of sklearn.compose.ColumnTransformer which returns the dataset as a pd.DataFrame
    and preserves readable feature names
    """

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        array = super(ColumnTransformer, self).fit_transform(X, y)
        return pd.DataFrame(array, index=X.index, columns=self.get_feature_names_out(self.feature_names_in_))

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        array = super(ColumnTransformer, self).transform(X)

        return pd.DataFrame(array, index=X.index, columns=self.get_feature_names_out(self.feature_names_in_))
