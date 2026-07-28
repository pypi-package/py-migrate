import pytest
from typer.testing import CliRunner
from pw_migrate.cli import app

runner = CliRunner()

def test_init_command():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Initializing pw-migrate environment" in result.stdout
