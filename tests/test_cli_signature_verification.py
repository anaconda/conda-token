import pytest
from conda_token.cli import signature_verification, token
from conda_token.repo_config import CONDA_VERSION, CondaVersionWarning
from packaging.version import parse


@pytest.mark.skipif(CONDA_VERSION < parse('4.10.1'), reason='Signature verification introduced in 4.10.1')
def test_enable_verification_without_token(remove_token, capsys):
    ret = signature_verification.cli(['--enable'])

    assert ret == 1
    captured = capsys.readouterr()
    assert captured.err == "You must first activate your subscription with 'conda token set <TOKEN>'\n"


@pytest.mark.skipif(CONDA_VERSION < parse('4.10.1'), reason='Signature verification introduced in 4.10.1')
def test_enable_verification_after_token(remove_token, secret_token, capsys):
    token.cli(['set', secret_token])
    ret = signature_verification.cli(['--enable'])

    assert ret == 0
    captured = capsys.readouterr()
    assert captured.out == 'Success! Your token was validated and Conda has been configured.\nConda package signature verification enabled.\n'


@pytest.mark.skipif(CONDA_VERSION >= parse('4.10.1'), reason='Signature verification introduced in 4.10.1')
def test_enable_verification_fail_old_conda(remove_token, capsys):
    ret = signature_verification.cli(['--enable'])

    assert ret == 1
    captured = capsys.readouterr()
    assert captured.err == 'You must first upgrade to at least Conda version 4.10.1.\n'