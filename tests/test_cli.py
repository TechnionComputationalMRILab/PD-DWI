from click.testing import CliRunner

from pd_dwi.scripts.cli import pd_dwi_cli


def test_cli_available():
    p = CliRunner().invoke(pd_dwi_cli, args=['--help'])
    assert not p.exit_code


def test_list():
    CliRunner().invoke(pd_dwi_cli, args=['list'])


def test_invalid_command():
    p = CliRunner().invoke(pd_dwi_cli, args=['cmd'])
    assert p.exit_code == 2


def test_predict(subtests):
    p = CliRunner().invoke(pd_dwi_cli, args=['predict'])
    assert p.exit_code == 2
