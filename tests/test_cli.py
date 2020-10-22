from conda_token import cli


def test_token_list(remove_token, capsys):
    ret = cli.cli(['list'])
    captured = capsys.readouterr()
    assert ret == 1
    assert captured.err == 'No tokens have been configured for https://repo.anaconda.cloud/repo/\n'
