# -*- coding: utf-8 -*-

from click.testing import CliRunner

from morpho.cli import cli


def test_cli_ensure_path_exists():
    runner = CliRunner()

    result = runner.invoke(cli, ["video", "/not/a/real/path"])

    assert result.exit_code == 1
    assert result.output == "ERROR: '/not/a/real/path' does not exist.\n"


def test_cli_requires_path():
    runner = CliRunner()

    result = runner.invoke(cli, ["audio"])

    assert result.exit_code == 2
    assert result.output.endswith('Error: Missing argument "PATH".\n')
