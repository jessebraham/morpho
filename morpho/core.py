# -*- coding: utf-8 -*-

import os
import subprocess

from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import List


class BaseFileFormat(Enum):
    """
    An abstract file-format Enum type. Contains properties wrapping the default
    'name' and 'value' attributes with 'codec' and 'extension' respectively.

    Additionally includes an abstract 'params' property, to be implemented by
    child classes, as well as a `get` method for obtaining the appropriate
    Enum value given a filesystem path.
    """

    @property
    def codec(self) -> str:
        return self.name

    @property
    def extension(self) -> str:
        return self.value

    @property
    @abstractmethod
    def params(self) -> List[str]:
        ...

    @classmethod
    def get(cls, path: str) -> "BaseFileFormat":
        (_, ext) = os.path.splitext(path)
        return cls(ext.lstrip("."))


class AudioFormat(BaseFileFormat):
    """
    An enumeration of supported audio file formats. The name and value
    attributes represent the file codec and extension respectively.
    """

    alac = "m4a"
    flac = "flac"

    @property
    def params(self) -> List[str]:
        return ["-c:a", self.codec]


class VideoFormat(BaseFileFormat):
    """
    An enumeration of supported video file formats. The name and value
    attributes represent the file codec and extension respectively.
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


def swap_extension(path: Path, fmt: BaseFileFormat) -> str:
    (head, _) = os.path.splitext(path)
    return f"{head}.{fmt.extension}"


class Ffmpeg:
    @classmethod
    def convert(cls, path: Path, fmt: BaseFileFormat) -> bool:
        command = cls.build_command(path, fmt)
        return cls.run(command)

    @staticmethod
    def build_command(path: Path, fmt: BaseFileFormat) -> List[str]:
        command = ["ffmpeg", "-i", str(path)]
        command += fmt.params
        command += [swap_extension(path, fmt)]
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
