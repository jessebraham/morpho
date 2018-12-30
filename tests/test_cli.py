# -*- coding: utf-8 -*-

from click.testing import CliRunner

from morpho.cli import cli, pluralized_file_count


def test_cli_requires_path_argument():
    runner = CliRunner()

    result = runner.invoke(cli, ["audio"])

    assert result.exit_code == 2
    assert result.output.endswith('Error: Missing argument "PATH".\n')


def test_cli_ensure_path_exists():
    runner = CliRunner()
    path = "/not/a/real/path"

    result = runner.invoke(cli, ["video", path])

    assert result.exit_code == 1
    assert result.output == f"ERROR: '{path}' does not exist.\n"


def test_cli_requires_non_empty_directory(tmpdir):
    runner = CliRunner()

    result = runner.invoke(cli, ["audio", str(tmpdir)])

    assert result.exit_code == 1
    assert result.output == "ERROR: No files found.\n"


def test_cli_pluralized_file_count():
    file_count_maybe_plural = pluralized_file_count(0)
    assert file_count_maybe_plural == "0 files"

    file_count_maybe_plural = pluralized_file_count(1)
    assert file_count_maybe_plural == "1 file"

    file_count_maybe_plural = pluralized_file_count(2)
    assert file_count_maybe_plural == "2 files"
