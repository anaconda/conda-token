import pytest
from conda.cli.python_api import Commands, run_command
from conda_token.repo_config import CondaTokenError, get_ssl_verify, token_list, validate_token
from requests import HTTPError

try:
    from conda.gateways.connection.session import CondaHttpAuth, CondaSession
except ImportError:
    from conda.connection import CondaHttpAuth, CondaSession


def test_add_token(set_dummy_token):
    assert token_list()['https://repo.anaconda.cloud/repo/'] == 'SECRET'

    base_url = 'https://repo.anaconda.cloud/repo/main/osx-64/repodata.json'
    token_url = 'https://repo.anaconda.cloud/t/SECRET/repo/main/osx-64/repodata.json'
    assert CondaHttpAuth.add_binstar_token(base_url) == token_url


def test_channeldata_403(remove_token):
    session = CondaSession()
    channeldata_url = 'https://repo.anaconda.cloud/repo/main/channeldata.json'
    r = session.get(channeldata_url)
    with pytest.raises(HTTPError):
        r.raise_for_status()
    assert r.status_code == 403


def test_repodata_200(set_secret_token):
    repodata_url = 'https://repo.anaconda.cloud/repo/main/osx-64/repodata.json'
    token_url = CondaHttpAuth.add_binstar_token(repodata_url)

    session = CondaSession()
    r = session.head(token_url)
    assert r.status_code == 200


def test_validate_token_error():
    with pytest.raises(CondaTokenError):
        validate_token('SECRET')


def test_validate_token_works(secret_token):
    assert validate_token(secret_token) is None


def test_conda_context():
    run_command(Commands.CONFIG, '--set', 'ssl_verify', 'false', use_exception_handler=True)
    assert not get_ssl_verify()
