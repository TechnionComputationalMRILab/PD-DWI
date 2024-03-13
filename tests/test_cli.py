from subprocess import run

import pytest

from pd_dwi.scripts.cli import pd_dwi_cli


def test_cli_available():
    p = run(["pd-dwi", "--help"])
    assert not p.returncode


def test_list():
    pd_dwi_cli(["list"])


def test_invalid_command():
    with pytest.raises(SystemExit):
        pd_dwi_cli(["cmd"])


def test_predict(subtests):
    with subtests.test("missing arguments"):
        with pytest.raises(SystemExit):
            pd_dwi_cli(["predict"])
