#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import subprocess
import sys
import time

from enum import Enum

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class FileFormat(Enum):
    alac = "m4a"
    flac = "flac"

    @property
    def codec(self) -> str:
        return self.name

    @property
    def extension(self) -> str:
        return self.value

    @classmethod
    def get(cls, extension: str) -> "FileFormat":
        return cls(extension.lower().lstrip("."))

    @classmethod
    def get_alternate(cls, extension: str) -> "FileFormat":
        ff = cls.get(extension)
        return FileFormat.alac if ff is FileFormat.flac else FileFormat.flac

    @classmethod
    def path_for_alternate(cls, path: str) -> str:
        (root, ext) = os.path.splitext(path)
        old_format = cls.get(ext)
        new_format = cls.get_alternate(ext)

        root = root.replace(
            os.sep.join(["", old_format.name, ""]),
            os.sep.join(["", new_format.name, ""]),
        )
        ext = new_format.extension
        return f"{root}.{ext}"

    @classmethod
    def alternate_exists(cls, path: str) -> bool:
        return os.path.exists(cls.path_for_alternate(path))


class Ffmpeg:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()

    async def convert_file(self, path: str, convert_to: FileFormat) -> None:
        write_path = FileFormat.path_for_alternate(path)
        command = ["ffmpeg", "-i", path, "-c:a", convert_to.codec, write_path]

        proc = await asyncio.create_subprocess_exec(
            *command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await proc.wait()

    def __call__(self, path: str, convert_to: FileFormat) -> None:
        self.loop.run_until_complete(
            asyncio.ensure_future(self.convert_file(path, convert_to))
        )
        self.loop.close()


class MorphoHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.converter = Ffmpeg()
        self.logger = logging.getLogger("morpho")

    def format_event(self, event):
        return f"{event.event_type}: '{event.src_path}'"

    def on_created(self, event):
        if not event.is_directory:
            self.logger.info(self.format_event(event))

    def on_deleted(self, event):
        if not event.is_directory:
            self.logger.info(self.format_event(event))

    def on_moved(self, event):
        self.logger.info(f"{self.format_event(event)} -> '{event.dest_path}'")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    event_handler = MorphoHandler()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
