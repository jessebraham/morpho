# -*- coding: utf-8 -*-

import asyncio
import logging
import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from morpho.core import AudioFormat, VideoFormat


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class Monitor:
    def __init__(self, max_queue_size: int = 0) -> None:
        logger = logging.getLogger("morpho")
        queue = asyncio.Queue(max_queue_size)  # type: asyncio.Queue
        self.event_handler = MorphoHandler(logger, queue)
        self.observer = Observer()
        self.worker = MorphoWorker(logger, queue)

    def register_path(self, path: str) -> None:
        self.observer.schedule(self.event_handler, path, recursive=True)

    def start(self) -> None:
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()


class MorphoHandler(FileSystemEventHandler):
    def __init__(self, logger: logging.Logger, queue: asyncio.Queue) -> None:
        self.logger = logger
        self.queue = queue

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return  # ignore directory creation

        if not self.has_valid_extension(event.src_path):
            return  # ignore unsupported file extensions

        self.logger.info(event)
        self.queue.put_nowait(event)

    def on_moved(self, event: FileSystemEvent) -> None:
        if not self.has_valid_extension(event.src_path):
            return  # ignore unsupported file extensions

        self.logger.info(event)
        self.queue.put_nowait(event)

    def has_valid_extension(self, path: str) -> bool:
        is_audio = AudioFormat.get(path) is not None
        is_video = VideoFormat.get(path) is not None
        return is_audio or is_video


class MorphoWorker:
    def __init__(self, logger: logging.Logger, queue: asyncio.Queue) -> None:
        self.logger = logger
        self.queue = queue
