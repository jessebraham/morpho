#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import os
import sys

from pathlib import Path
from typing import List

from morpho.core import BaseFileFormat, AudioFormat, Ffmpeg, VideoFormat


def ensure_path_exists(path: Path) -> None:
    if not os.path.exists(path):
        click.secho(f"ERROR: '{path}' does not exist.", fg="red")
        sys.exit(1)


def find_media(path: Path, fmt: BaseFileFormat) -> List[Path]:
    audio_extensions = [f.extension for f in AudioFormat]
    video_extensions = [f.extension for f in VideoFormat]
    extensions = [
        f for f in audio_extensions + video_extensions if f != fmt.extension
    ]

    return [
        f
        for extension in extensions
        for f in path.rglob(f"*.{extension}")
    ]


def get_file_list(path: Path, fmt: BaseFileFormat) -> List[Path]:
    if os.path.isdir(path):
        files = find_media(path, fmt)
    elif os.path.isfile(path):
        files = [path]
    else:
        files = []
    return files


def convert(path: str, fmt: BaseFileFormat) -> None:
    ensure_path_exists(Path(path))

    files = get_file_list(Path(path), fmt)
    if not files:
        click.secho("No files found.", fg="red")
        return

    click.secho(f"Found {len(files)} file(s).", fg="green")

    for f in files:
        click.echo(f"Converting '{f}' to {fmt.codec}")
        Ffmpeg.convert(f, fmt)

    click.secho(f"Converted {len(files)} file(s)!", fg="green")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path")
@click.option(
    "--codec", type=click.Choice(["alac", "flac"]), help="Output codec."
)
def audio(path, codec) -> None:
    fmt = AudioFormat.get(codec)
    convert(path, fmt)


@cli.command()
@click.argument("path")
def video(path) -> None:
    fmt = VideoFormat.mp4
    convert(path, fmt)


if __name__ == "__main__":
    cli()
