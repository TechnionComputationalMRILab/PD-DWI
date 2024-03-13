from argparse import ArgumentError
from subprocess import run

import pytest

from pd_dwi.scripts.cli import pd_dwi_cli


def test_cli_available():
    p = run(["pd-dwi", "--help"])
    assert not p.returncode


def test_list():
    pd_dwi_cli(["list"])
    

def test_predict(subtests):
    with subtests.test("missing arguments"):
        with pytest.raises(TypeError):
            pd_dwi_cli(["predict"])
