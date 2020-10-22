import os

import pytest
from conda.gateways.connection.session import CondaHttpAuth, CondaSession
from requests import HTTPError

from conda_token.repo_config import token_list, token_remove, token_set


@pytest.fixture(scope='function')
def remove_token():
    token_remove()
    yield
    token_remove()


def test_add_token(remove_token):
    tokens = token_list()
    token_set('SECRET')
    tokens['https://repo.anaconda.cloud/repo/'] = 'SECRET'

    assert token_list() == tokens

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


def test_channeldata_200(remove_token):
    secret_token = os.environ.get('CE_TOKEN', False)
    if not secret_token:
        return

    token_set('fc96b40a762d3826b7d958114336549769188541017cc3ef')
    repodata_url = 'https://repo.anaconda.cloud/repo/main/osx-64/repodata.json'
    token_url = CondaHttpAuth.add_binstar_token(repodata_url)
    print(token_url)

    session = CondaSession()
    r = session.head(token_url)
    assert r.status_code == 200
