import pytest
import json

from packaging.version import parse

from conda.cli.python_api import Commands, run_command
from conda_token.repo_config import CONDA_VERSION


@pytest.mark.skipif(CONDA_VERSION < parse('4.10.1'), reason='Signature verification was added in Conda 4.10.1')
def test_conda_search_rope_signed(set_secret_token_with_signing):
    stdout, _, _ = run_command(Commands.SEARCH, '--spec', 'rope=0.18.0=py_0', '--json')
    rope = json.loads(stdout)['rope'][0]
    assert rope['metadata_signature_status'] == 0

    stdout, _, _ = run_command(Commands.SEARCH, '--spec', 'conda-forge::rope=0.18.0=pyhd3deb0d_0', '--json')
    rope = json.loads(stdout)['rope'][0]
    assert rope['metadata_signature_status'] == -1


def test_conda_search_rope(set_secret_token):
    if CONDA_VERSION < parse('4.4'):
        stdout, _, _ = run_command(Commands.SEARCH, '--spec', 'rope=0.18.0=py_0', '--json')
    else:
        stdout, _, _ = run_command(Commands.SEARCH, 'rope==0.18.0=py_0', '--json')
    rope = json.loads(stdout)['rope'][0]
    assert rope['url'].startswith('https://repo.anaconda.cloud/repo/main/noarch')


def test_conda_install_rope(set_secret_token, uninstall_rope):
    run_command(Commands.INSTALL, 'rope', '-y')

    if CONDA_VERSION < parse('4.6'):
        stdout, _, _ = run_command(Commands.LIST, '--explicit')
        pkgs = stdout.splitlines()
        for p in pkgs:
            if 'rope' in p:
                assert p.startswith('https://repo.anaconda.cloud/repo/main')
    else:
        stdout, _, _ = run_command(Commands.LIST, 'rope', '--show-channel-urls', '--json')
        rope = json.loads(stdout)[0]
        assert rope['base_url'] == 'https://repo.anaconda.cloud/repo/main'


def test_conda_install_with_conda_forge(set_secret_token, uninstall_rope, uninstall_colorama):
    run_command(Commands.INSTALL, '-c', 'defaults', '-c', 'conda-forge', 'rope', 'conda-forge-pinning', '-y')

    if CONDA_VERSION < parse('4.6'):
        stdout, _, _ = run_command(Commands.LIST, '--explicit')
        pkgs = stdout.splitlines()
        for p in pkgs:
            if 'rope' in p:
                assert p.startswith('https://repo.anaconda.cloud/repo/main')
            if 'conda-forge-pinning' in p:
                assert p.startswith('https://conda.anaconda.org/conda-forge')
    else:
        stdout, _, _ = run_command(Commands.LIST, 'rope', '--show-channel-urls', '--json')
        rope = json.loads(stdout)[0]
        assert rope['base_url'] == 'https://repo.anaconda.cloud/repo/main'

        stdout, _, _ = run_command(Commands.LIST, 'conda-forge-pinning', '--show-channel-urls', '--json')
        conda_forge_pinning = json.loads(stdout)[0]
        assert conda_forge_pinning['base_url'] == 'https://conda.anaconda.org/conda-forge'
