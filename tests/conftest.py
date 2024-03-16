import os

import pytest


@pytest.fixture(scope="function")
def test_data(request):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, f'./data/{request.param}.yaml')
