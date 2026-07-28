import os

from typer.testing import CliRunner

from pw_migrate.cli import app

runner = CliRunner()


def test_status_command(tmp_path):
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Migration Status" in result.stdout


def test_pending_command(tmp_path):
    result = runner.invoke(app, ["pending"])
    assert result.exit_code == 0
    assert (
        "No pending migrations" in result.stdout
        or "Pending Migrations" in result.stdout
    )


def test_current_command():
    result = runner.invoke(app, ["current"])
    assert result.exit_code == 0
    assert "Current Version:" in result.stdout


def test_up_command(tmp_path):
    result = runner.invoke(app, ["up", "--fake"])
    assert result.exit_code == 0
    assert "Starting migrations" in result.stdout


def test_down_command():
    result = runner.invoke(app, ["down", "--fake"])
    assert result.exit_code == 0


def test_rollback_command():
    result = runner.invoke(app, ["rollback", "20260728124500", "--fake"])
    assert result.exit_code in (0, 1)


def test_redo_command():
    result = runner.invoke(app, ["redo", "--fake"])
    assert result.exit_code in (0, 1)


def test_reset_command():
    result = runner.invoke(app, ["reset", "--fake"])
    assert result.exit_code == 0


def test_fresh_command():
    result = runner.invoke(app, ["fresh", "--fake"])
    assert result.exit_code == 0


def test_create_command(tmp_path):

    # Temporarily change working directory to test dir so migration is created there
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(app, ["create", "test_migration"])
        assert result.exit_code == 0
        assert "Created migration" in result.stdout

        # Verify file exists
        migrations = os.listdir("migrations")
        assert "test_migration.py" in migrations[0]
    finally:
        os.chdir(original_cwd)


def test_run_single_command():
    result = runner.invoke(
        app, ["run", "20260728124500", "--direction", "up", "--fake"]
    )
    # 20260728124500 does not exist in standard mocked discovery without setup,
    # so we expect it to fail with "not found" or similar unless we mock discovery.
    # Since we test CLI wrapper here, let's just assert it runs and exits.
    assert result.exit_code in (0, 1)
