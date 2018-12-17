# -*- coding: utf-8 -*-

import os

from enum import Enum
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

    def update_extension(self, path: str) -> str:
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
            "-pre",
            "fast",
        ]
        return audio_params + video_params
