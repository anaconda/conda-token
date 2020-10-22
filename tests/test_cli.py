from conda_token import cli

def test_cli_template():
    assert cli.cli() is None
