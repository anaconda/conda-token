import os
import warnings
from unittest import mock

import pytest
from conda_token.conda_api import Commands, run_command

from conda_token.repo_config import clean_index, token_remove, token_set


def pytest_configure(config):
    warnings.filterwarnings("always")


@pytest.fixture(scope="session", autouse=True)
def reset_channels_alias():
    clean_index()
    run_command(Commands.CONFIG, "--remove-key", "channels", use_exception_handler=True)
    run_command(
        Commands.CONFIG, "--prepend", "channels", "defaults", use_exception_handler=True
    )
    run_command(
        Commands.CONFIG,
        "--set",
        "channel_alias",
        "https://conda.anaconda.org",
        use_exception_handler=True,
    )


@pytest.fixture(scope="function", autouse=True)
def set_ssl_verify_true():
    run_command(
        Commands.CONFIG, "--set", "ssl_verify", "true", use_exception_handler=True
    )
    yield
    run_command(
        Commands.CONFIG, "--set", "ssl_verify", "true", use_exception_handler=True
    )


@pytest.fixture(scope="function")
def remove_token(repo_url):
    token_remove()
    yield
    token_remove()


@pytest.fixture(scope="function")
def remove_anaconda_cloud_token():
    """
    Remove token without mock repo_url
    """
    token_remove()
    yield
    token_remove()


@pytest.fixture(scope="function")
def set_dummy_token(repo_url):
    token_remove()
    token_set("SECRET")
    yield
    token_remove()


@pytest.fixture(scope="function")
def set_secret_token():
    token_remove()
    secret_token = os.environ.get("CE_TOKEN", "")
    token_set(secret_token)
    yield
    token_remove()


@pytest.fixture(scope="function")
def set_secret_token_mock_server(repo_url):
    token_remove()
    secret_token = os.environ.get("CE_TOKEN", "")
    token_set(secret_token)
    yield
    token_remove()


@pytest.fixture(scope="function")
def set_secret_token_with_signing():
    token_remove()
    secret_token = os.environ.get("CE_TOKEN", "")
    token_set(secret_token, enable_signature_verification=True)
    yield
    token_remove()


@pytest.fixture(scope="function")
def secret_token():
    token = os.environ.get("CE_TOKEN", "")
    yield token


@pytest.fixture(scope="function")
def uninstall_rope():
    run_command(Commands.REMOVE, "rope", "-y", use_exception_handler=True)
    yield
    run_command(Commands.REMOVE, "rope", "-y", use_exception_handler=True)


@pytest.fixture(scope="function")
def uninstall_colorama():
    run_command(Commands.REMOVE, "colorama", "-y", use_exception_handler=True)
    yield
    run_command(Commands.REMOVE, "colorama", "-y", use_exception_handler=True)


@pytest.fixture
def channeldata_url(repo_url):
    return repo_url + "main/channeldata.json"


@pytest.fixture
def repodata_url(repo_url):
    return repo_url + "main/osx-64/repodata.json"


@pytest.fixture
def repo_url(test_server_url):
    repo_url = test_server_url + "/repo/"
    with mock.patch.dict(os.environ, {"CONDA_TOKEN_REPO_URL": repo_url}):
        with mock.patch("conda_token.repo_config.REPO_URL", repo_url):
            yield repo_url


@pytest.fixture(scope="session")
def test_server_url():
    from . import testing_server

    return testing_server.run_server()
