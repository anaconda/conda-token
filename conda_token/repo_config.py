from os.path import abspath, expanduser, join
from urllib.parse import urljoin
import sys

import conda.gateways.logging  # noqa: F401
from conda.cli.python_api import Commands, run_command
from conda.exceptions import CondaKeyError
from conda.gateways.anaconda_client import (read_binstar_tokens, remove_binstar_token,
                                            set_binstar_token)

REPO_URL = 'https://repo.anaconda.cloud/repo/'
MAIN_CHANNEL = 'main'
ACTIVE_CHANNELS = ['r', 'msys2']
ARCHIVE_CHANNELS = ['free', 'mro', 'mro-archive', 'pro']

user_rc_path = abspath(expanduser('~/.condarc'))
escaped_user_rc_path = user_rc_path.replace("%", "%%")
escaped_sys_rc_path = abspath(join(sys.prefix, '.condarc')).replace("%", "%%")


def clean_index():
    run_command(Commands.CLEAN, '-i')


def _set_channel(channel, prepend=True, condarc_system=None, condarc_env=None, condarc_file=None):
    channel_url = urljoin(REPO_URL, channel)

    config_args = [
        '--prepend' if prepend else '--append',
        'default_channels',
        channel_url
    ]

    if condarc_system:
        config_args.append('--system')
    elif condarc_env:
        config_args.append('--env')
    elif condarc_file:
        config_args.append('--file={}'.format(condarc_file))

    run_command(Commands.CONFIG, *config_args)


def _remove_default_channels(condarc_system=None, condarc_env=None, condarc_file=None):
    config_args = ['--remove-key', 'default_channels']

    if condarc_system:
        config_args.append('--system')
    elif condarc_env:
        config_args.append('--env')
    elif condarc_file:
        config_args.append('--file={}'.format(condarc_file))

    try:
        run_command(Commands.CONFIG, *config_args)
    except CondaKeyError:
        pass


def configure_default_channels(condarc_system=None, condarc_env=None, condarc_file=None,
                               include_archive_channels=None):
    _remove_default_channels(condarc_system, condarc_env, condarc_file)

    _set_channel(MAIN_CHANNEL, prepend=True,
                 condarc_system=condarc_system, condarc_env=condarc_env, condarc_file=condarc_file)

    for c in ACTIVE_CHANNELS:
        _set_channel(c, prepend=False,
                     condarc_system=condarc_system, condarc_env=condarc_env, condarc_file=condarc_file)

    if include_archive_channels is None:
        return

    for c in include_archive_channels:
        if c in ARCHIVE_CHANNELS:
            _set_channel(c, prepend=False,
                         condarc_system=condarc_system, condarc_env=condarc_env, condarc_file=condarc_file)
        else:
            raise ValueError('The archive channel %s is not one of %s' % (c, ', '.join(ARCHIVE_CHANNELS)))


def token_list():
    return read_binstar_tokens()


def token_remove():
    remove_binstar_token(REPO_URL)
    _remove_default_channels()
    clean_index()


def token_set(token, system=None, env=None, file=None, include_archive_channels=None):
    remove_binstar_token(REPO_URL)

    set_binstar_token(REPO_URL, token)
    configure_default_channels(system, env, file, include_archive_channels)
    clean_index()
