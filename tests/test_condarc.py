from contextlib import contextmanager
from packaging import version
from tempfile import NamedTemporaryFile

from conda.base.context import reset_context
from conda.gateways.disk.delete import rm_rf

from conda_token.repo_config import configure_default_channels, CONDA_VERSION


@contextmanager
def make_temp_condarc(value=None):
    try:
        tempfile = NamedTemporaryFile(suffix='.yml', delete=False)
        tempfile.close()
        temp_path = tempfile.name
        if value:
            with open(temp_path, 'w') as f:
                f.write(value)
        reset_context([temp_path])
        yield temp_path
    finally:
        rm_rf(temp_path)


def _read_test_condarc(rc):
    with open(rc) as f:
        return f.read()


def test_default_channels():
    empty_condarc = '\n'
    final_condarc = """\
default_channels:
  - https://repo.anaconda.cloud/repo/main
  - https://repo.anaconda.cloud/repo/r
  - https://repo.anaconda.cloud/repo/msys2
"""
    if not (CONDA_VERSION < version.parse('4.7')):
        final_condarc = 'restore_free_channel: false\n' + final_condarc

    with make_temp_condarc(empty_condarc) as rc:
        configure_default_channels(condarc_file=rc)
        assert _read_test_condarc(rc) == final_condarc


def test_replace_default_channels():
    original_condarc = """\
default_channels:
  - https://repo.anaconda.com/pkg/main
  - https://repo.anaconda.com/pkg/r
  - https://repo.anaconda.com/pkg/msys2
"""
    final_condarc = """\
default_channels:
  - https://repo.anaconda.cloud/repo/main
  - https://repo.anaconda.cloud/repo/r
  - https://repo.anaconda.cloud/repo/msys2
"""
    if not (CONDA_VERSION < version.parse('4.7')):
        final_condarc = 'restore_free_channel: false\n' + final_condarc

    with make_temp_condarc(original_condarc) as rc:
        configure_default_channels(condarc_file=rc)
        assert _read_test_condarc(rc) == final_condarc


def test_default_channels_with_inactive():
    original_condarc = """\
default_channels:
  - https://repo.anaconda.com/pkg/main
  - https://repo.anaconda.com/pkg/r
  - https://repo.anaconda.com/pkg/msys2
"""
    final_condarc = """\
default_channels:
  - https://repo.anaconda.cloud/repo/main
  - https://repo.anaconda.cloud/repo/r
  - https://repo.anaconda.cloud/repo/msys2
  - https://repo.anaconda.cloud/repo/free
  - https://repo.anaconda.cloud/repo/pro
  - https://repo.anaconda.cloud/repo/mro
  - https://repo.anaconda.cloud/repo/mro-archive
"""
    if not (CONDA_VERSION < version.parse('4.7')):
        final_condarc = 'restore_free_channel: false\n' + final_condarc

    with make_temp_condarc(original_condarc) as rc:
        configure_default_channels(condarc_file=rc, include_archive_channels=['free', 'pro', 'mro', 'mro-archive'])
        assert _read_test_condarc(rc) == final_condarc


def test_replace_default_channels_with_inactive():
    empty_condarc = '\n'
    final_condarc = """\
default_channels:
  - https://repo.anaconda.cloud/repo/main
  - https://repo.anaconda.cloud/repo/r
  - https://repo.anaconda.cloud/repo/msys2
  - https://repo.anaconda.cloud/repo/free
  - https://repo.anaconda.cloud/repo/pro
  - https://repo.anaconda.cloud/repo/mro
  - https://repo.anaconda.cloud/repo/mro-archive
"""
    if not (CONDA_VERSION < version.parse('4.7')):
        final_condarc = 'restore_free_channel: false\n' + final_condarc

    with make_temp_condarc(empty_condarc) as rc:
        configure_default_channels(condarc_file=rc, include_archive_channels=['free', 'pro', 'mro', 'mro-archive'])
        assert _read_test_condarc(rc) == final_condarc


def test_default_channels_with_conda_forge():
    if not (CONDA_VERSION < version.parse('4.7')):
        original_condarc = """\
ssl_verify: true
restore_free_channel: true

default_channels:
  - https://repo.anaconda.com/pkgs/main
channels:
  - defaults
  - conda-forge

channel_alias: https://conda.anaconda.org/
"""

        with make_temp_condarc(original_condarc) as rc:
            configure_default_channels(condarc_file=rc)
            assert _read_test_condarc(rc) == """\
ssl_verify: true
restore_free_channel: false

channels:
  - defaults
  - conda-forge

channel_alias: https://conda.anaconda.org/
default_channels:
  - https://repo.anaconda.cloud/repo/main
  - https://repo.anaconda.cloud/repo/r
  - https://repo.anaconda.cloud/repo/msys2
"""
    else:
        original_condarc = """\
ssl_verify: true

default_channels:
  - https://repo.anaconda.com/pkgs/main
channels:
  - defaults
  - conda-forge

channel_alias: https://conda.anaconda.org/
"""

        with make_temp_condarc(original_condarc) as rc:
            configure_default_channels(condarc_file=rc)
            assert _read_test_condarc(rc) == """\
ssl_verify: true

channels:
  - defaults
  - conda-forge

channel_alias: https://conda.anaconda.org/
default_channels:
  - https://repo.anaconda.cloud/repo/main
  - https://repo.anaconda.cloud/repo/r
  - https://repo.anaconda.cloud/repo/msys2
"""
