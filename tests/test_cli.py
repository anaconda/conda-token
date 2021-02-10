import warnings

import pytest
import urllib3.exceptions
from conda_token import cli


def test_token_set_no_verify_ssl(remove_token, secret_token, capsys):
    with pytest.warns(urllib3.exceptions.InsecureRequestWarning):
        cli.cli(['set', '--no-ssl-verify', secret_token])

    ret = cli.cli(['list'])
    assert ret == 0
    captured = capsys.readouterr()
    assert captured.out == 'https://repo.anaconda.cloud/repo/ %s\n' % secret_token


def test_token_list(remove_token, capsys):
    ret = cli.cli(['list'])
    captured = capsys.readouterr()
    assert ret == 1
    assert captured.err == 'No tokens have been configured for https://repo.anaconda.cloud/repo/\n'


def test_token_set_invalid_channel(remove_token):
    with pytest.raises(SystemExit):
        cli.cli(['set', 'secret', '--include-archive-channels', 'nope'])


def test_token_set(remove_token, secret_token, capsys):
    cli.cli(['set', secret_token])

    ret = cli.cli(['list'])
    assert ret == 0
    captured = capsys.readouterr()
    assert captured.out == 'https://repo.anaconda.cloud/repo/ %s\n' % secret_token


def test_token_set_error(remove_token, capsys):
    ret = cli.cli(['set', 'SECRET'])
    assert ret == 1
    captured = capsys.readouterr()
    assert captured.err == 'The token could not be validated. Please check that you have typed it correctly.\n'

    ret = cli.cli(['list'])
    assert ret == 1
    captured = capsys.readouterr()
    assert captured.err == 'No tokens have been configured for https://repo.anaconda.cloud/repo/\n'
