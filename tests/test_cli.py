import pytest

from conda_token import cli


def test_token_list(remove_token, capsys):
    ret = cli.cli(['list'])
    captured = capsys.readouterr()
    assert ret == 1
    assert captured.err == 'No tokens have been configured for https://repo.anaconda.cloud/repo/\n'


def test_token_set_invalid_channel(remove_token):
    with pytest.raises(SystemExit):
        cli.cli(['set', 'secret', '--include-archive-channels', 'nope'])


def test_token_set(remove_token, capsys):
    cli.cli(['set', 'SECRET'])

    ret = cli.cli(['list'])
    assert ret == 0
    captured = capsys.readouterr()
    assert captured.out == 'https://repo.anaconda.cloud/repo/ SECRET\n'

