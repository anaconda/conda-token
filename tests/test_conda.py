import json

from conda.cli.python_api import Commands, run_command


def test_conda_search_rope(set_secret_token):
    stdout, _, _ = run_command(Commands.SEARCH, 'rope==0.18.0=py_0', '--json')
    rope = json.loads(stdout)['rope'][0]
    assert rope['channel'] == 'https://repo.anaconda.cloud/repo/main/noarch'


def test_conda_install_rope(set_secret_token, uninstall_rope):
    run_command(Commands.INSTALL, 'rope', '-y')

    stdout, _, _ = run_command(Commands.LIST, 'rope', '--show-channel-urls', '--json')
    rope = json.loads(stdout)[0]
    if rope['base_url'] is None:
        assert rope['channel'] == 'https://repo.anaconda.cloud/repo/main'
    else:
        assert rope['base_url'] == 'https://repo.anaconda.cloud/repo/main'


def test_conda_install_with_conda_forge(set_secret_token, uninstall_rope, uninstall_colorama):
    run_command(Commands.INSTALL, 'defaults::rope', 'conda-forge::colorama', '-y')

    stdout, _, _ = run_command(Commands.LIST, 'rope', '--show-channel-urls', '--json')
    rope = json.loads(stdout)[0]
    if rope['base_url'] is None:
        assert rope['channel'] == 'https://repo.anaconda.cloud/repo/main'
    else:
        assert rope['base_url'] == 'https://repo.anaconda.cloud/repo/main'

    stdout, _, _ = run_command(Commands.LIST, 'colorama', '--show-channel-urls', '--json')
    rope = json.loads(stdout)[0]
    if rope['base_url'] is None:
        assert rope['channel'] == 'conda-forge'
    else:
        assert rope['base_url'] == 'https://conda.anaconda.org/conda-forge'
