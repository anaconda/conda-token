import os
import pytest

from conda.cli.python_api import Commands, run_command

from conda_token.repo_config import token_remove, token_set


@pytest.fixture(scope='session', autouse=True)
def reset_channels_alias():
    run_command(Commands.CONFIG, '--remove-key', 'channels', use_except_handler=True)
    run_command(Commands.CONFIG, '--prepend', 'channels', 'defaults', use_except_handler=True)
    run_command(Commands.CONFIG, '--set', 'channel_alias', 'https://conda.anaconda.org', use_exception_handler=True)


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


@pytest.fixture(scope='function')
def secret_token():
    token = os.environ.get('CE_TOKEN', '')
    yield token


@pytest.fixture(scope='function')
def uninstall_rope():
    run_command(Commands.REMOVE, 'rope', '-y', use_exception_handler=True)
    yield
    run_command(Commands.REMOVE, 'rope', '-y', use_exception_handler=True)


@pytest.fixture(scope='function')
def uninstall_colorama():
    run_command(Commands.REMOVE, 'colorama', '-y', use_exception_handler=True)
    yield
    run_command(Commands.REMOVE, 'colorama', '-y', use_exception_handler=True)
