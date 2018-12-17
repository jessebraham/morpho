#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import os
import sys

from pathlib import Path
from typing import List

from morpho.core import BaseFileFormat, AudioFormat, VideoFormat
from morpho.core import Ffmpeg


def ensure_path_exists(path: str) -> None:
    if not os.path.exists(path):
        click.secho(f"ERROR: '{path}' does not exist.", fg="red")
        sys.exit(1)


def find_media(path: str, fmt: BaseFileFormat) -> List[str]:
    audio_extensions = [f.extension for f in AudioFormat]
    video_extensions = [f.extension for f in VideoFormat]
    extensions = [
        f for f in audio_extensions + video_extensions if f != fmt.extension
    ]

    return [
        f
        for extension in extensions
        for f in Path(path).rglob(f"*.{extension}")
    ]


def convert_files(path: str, fmt: BaseFileFormat) -> None:
    if os.path.isdir(path):
        files = find_media(path, fmt)
    elif os.path.isfile(path):
        files = [path]
    else:
        files = []

    click.secho(f"Found {len(files)} file(s).", fg="green")
    if not files:
        return

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
def audio(path, codec):
    ensure_path_exists(path)
    fmt = AudioFormat.get(codec)
    convert_files(path, fmt)


@cli.command()
@click.argument("path")
def video(path):
    ensure_path_exists(path)
    fmt = VideoFormat.mp4
    convert_files(path, fmt)


if __name__ == "__main__":
    cli()
