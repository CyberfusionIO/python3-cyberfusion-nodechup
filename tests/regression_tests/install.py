from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from cyberfusion.Nodechup.CLI import app
from cyberfusion.Nodechup.nodejs import NodeJSAlreadyInstalled

runner = CliRunner()

# compatibility test fixture
ARGS = ["install", "--version=22.17.1", "--update-default-version"]


def test_install(tmp_path: Path, mocker: MockerFixture) -> None:
    download = mocker.patch("cyberfusion.Nodechup.CLI.Installation.download")

    result = runner.invoke(app, [*ARGS, f"--base-directory-path={tmp_path}"])

    assert result.exit_code == 0, result.output

    download.assert_called_once_with(update_default_version=True)


def test_install_already_installed(tmp_path: Path, mocker: MockerFixture) -> None:
    mocker.patch(
        "cyberfusion.Nodechup.CLI.Installation.download",
        side_effect=NodeJSAlreadyInstalled(str(tmp_path)),
    )

    result = runner.invoke(app, [*ARGS, f"--base-directory-path={tmp_path}"])

    assert result.exit_code == 78
    assert "already exists" in result.output
