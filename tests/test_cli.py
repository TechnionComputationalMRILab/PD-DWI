from subprocess import run


def test_cli_available():
    p = run(["pd-dwi", "help"])
    assert not p.returncode
