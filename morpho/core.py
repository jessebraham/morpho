# -*- coding: utf-8 -*-

import os
import subprocess

from enum import Enum
from pathlib import Path
from typing import List


class BaseFileFormat(Enum):
    """
    A generic file format Enum type, with properties wrapping the default
    'name' and 'value' attributes with 'codec' and 'extension' respectively.

    Additionally includes a handful of common helper functions.
    """

    @property
    def codec(self) -> str:
        return self.name

    @property
    def extension(self) -> str:
        return self.value

    @property
    def params(self) -> List[str]:
        pass

    def update_extension(self, path: Path) -> str:
        (head, _) = os.path.splitext(path)
        return f"{head}.{self.extension}"

    @classmethod
    def get(cls, path: str) -> "BaseFileFormat":
        (_, ext) = os.path.splitext(path)
        return cls(ext.lstrip("."))


class AudioFormat(BaseFileFormat):
    """
    An enumeration of Audio file formats. The name represents the codec while
    the value holds its extension.
    """

    alac = "m4a"
    flac = "flac"

    @property
    def params(self) -> List[str]:
        return ["-c:a", self.codec]


class VideoFormat(BaseFileFormat):
    """
    An enumeration of Video file formats. The name represents the codec while
    the value holds its extension.
    """

    avi = "avi"
    mp4 = "mp4"
    mkv = "mkv"

    @property
    def params(self) -> List[str]:
        audio_params = ["-c:a", "aac", "-b:a", "192k"]
        video_params = [
            "-f",
            "mp4",
            "-c:v",
            "libx264",
            "-profile:v",
            "main",
            "-preset",
            "fast",
        ]
        return audio_params + video_params


class Ffmpeg:
    @staticmethod
    def build_command(path: Path, fmt: BaseFileFormat) -> List[str]:
        command = ["ffmpeg", "-i", str(path)]
        command += fmt.params
        command += [fmt.update_extension(path)]
        return command

    @staticmethod
    def run(command: List[str]) -> bool:
        try:
            p = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return p.returncode == 0
        except Exception:
            return False

    @classmethod
    def convert(cls, path: Path, fmt: BaseFileFormat) -> bool:
        command = cls.build_command(path, fmt)
        return cls.run(command)
