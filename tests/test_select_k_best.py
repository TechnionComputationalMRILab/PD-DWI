import pandas as pd

from pd_dwi.feature_selection.select_k_best import SelectKBest


def test_select_k_best():
    X = pd.DataFrame.from_dict({
        'A': [0, 1, 0],
        'B': [1, 2, 3],
        'C': [3, 3, 3],
    })

    y = X['A'].copy()

    fs = SelectKBest(k=1)
    X_out = fs.fit_transform(X, y)
    assert X_out.shape[1] == fs.k
    assert X_out.columns == ['A']


