#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from pathlib import Path
from typing import List

from morpho.core import BaseFileFormat, AudioFormat, VideoFormat
from morpho.core import Ffmpeg


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


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path")
@click.option(
    "--codec", type=click.Choice(["alac", "flac"]), help="Output codec."
)
def audio(path, codec):
    fmt = AudioFormat.get(codec)
    files = find_media(path, fmt)

    for f in files:
        click.echo(f"Converting '{f}' to {fmt.codec}")
        Ffmpeg.convert(f, fmt)


@cli.command()
@click.argument("path")
def video(path):
    fmt = VideoFormat.mp4
    files = find_media(path, fmt)

    for f in files:
        click.echo(f"Converting '{f}' to {fmt.codec}")
        Ffmpeg.convert(f, fmt)


if __name__ == "__main__":
    cli()
