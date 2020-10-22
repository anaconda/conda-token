import os
import pytest

from conda_token.repo_config import token_remove, token_set


@pytest.fixture(scope='function')
def remove_token():
    token_remove()
    yield
    token_remove()


@pytest.fixture(scope='function')
def set_dummy_token():
    token_remove()
    token_set('SECRET')
    yield
    token_remove()


@pytest.fixture(scope='function')
def set_secret_token():
    token_remove()
    secret_token = os.environ.get('CE_TOKEN', '')
    token_set(secret_token)
    yield
    token_remove()
