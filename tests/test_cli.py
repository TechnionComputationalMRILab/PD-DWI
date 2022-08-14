from subprocess import run


def test_cli_available():
    p = run(["pd-dwi", "list"])
    assert not p.returncode
