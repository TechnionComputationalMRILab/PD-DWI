from subprocess import run


def test_cli_available():
    p = run(["pd-dwi"])
    assert not p.returncode
