import pytest
from requests import HTTPError
from urllib3.exceptions import InsecureRequestWarning

from conda_token.repo_config import token_list, validate_token, CondaTokenError

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


def test_channeldata_200(set_secret_token):
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


def test_validate_token_works_no_ssl(secret_token):
    with pytest.warns(InsecureRequestWarning):
        assert validate_token(secret_token, ssl_verify=False) is None
