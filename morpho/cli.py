#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import os
import sys

import inflect

from pathlib import Path
from typing import List

from morpho.core import AudioFormat, BaseFileFormat, Ffmpeg, VideoFormat


def convert(path: Path, convert_to: BaseFileFormat) -> None:
    if not os.path.exists(path):
        click.secho(f"ERROR: '{path}' does not exist.", fg="red")
        sys.exit(1)

    files = get_file_list(path, convert_to)
    if not files:
        click.secho("ERROR: No files found.", fg="red")
        sys.exit(1)

    file_count_maybe_plural = pluralized_file_count(len(files))
    click.secho(f"Found {file_count_maybe_plural}.", fg="green")

    converted_files = 0
    for f in files:
        click.echo(f"Converting '{f}' to {convert_to.codec}.")
        if Ffmpeg.convert(f, convert_to):
            converted_files += 1
        else:
            click.secho(f"Unable to convert '{f}' to {convert_to.codec}.")

    file_count_maybe_plural = pluralized_file_count(converted_files)
    click.secho(f"Converted {file_count_maybe_plural}.", fg="green")


def get_file_list(path: Path, convert_to: BaseFileFormat) -> List[Path]:
    if os.path.isdir(path):
        files = find_media(path, convert_to)
    else:
        files = [path]
    return files


def find_media(path: Path, convert_to: BaseFileFormat) -> List[Path]:
    extensions = [f.extension for f in type(convert_to) if f != convert_to]
    return [f for extension in extensions for f in path.rglob(f"*.{extension}")]


def pluralized_file_count(count: int) -> str:
    e = inflect.engine()
    return f"{count} {e.plural('file', count)}"


# -----------------------------------------------------------------------------
# Commands


@click.group()
def cli():
    ...


@cli.command()
@click.argument("path")
def audio(path: str) -> None:
    convert_to = (
        AudioFormat.alac
        if AudioFormat.get(path) == AudioFormat.flac
        else AudioFormat.flac
    )
    convert(Path(path), convert_to)


@cli.command()
@click.argument("path")
def video(path: str) -> None:
    # For the time being, always convert videos to mp4.
    convert(Path(path), VideoFormat.mp4)


if __name__ == "__main__":
    cli()
