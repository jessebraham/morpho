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
        self.logger = logging.getLogger("morpho")
        queue = asyncio.Queue(max_queue_size)  # type: asyncio.Queue

        self.event_handler = MorphoHandler(self.logger, queue)
        self.observer = Observer()
        self.worker = MorphoWorker(self.logger, queue)

    def register_path(self, path: str) -> None:
        self.observer.schedule(self.event_handler, path, recursive=True)

    def start(self) -> None:
        self.observer.start()
        self.logger.info("Starting monitor")

        try:
            while True:
                self.worker.process_event_from_queue()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt received, terminating")
            self.observer.stop()

        self.observer.join()


class MorphoHandler(FileSystemEventHandler):
    def __init__(self, logger: logging.Logger, queue: asyncio.Queue) -> None:
        self.logger = logger
        self.queue = queue

    def on_created(self, event: FileSystemEvent) -> None:
        # ignore directory creation
        if not event.is_directory:
            self.handle_event(event)

    def on_moved(self, event: FileSystemEvent) -> None:
        self.handle_event(event)

    def handle_event(self, event: FileSystemEvent) -> None:
        # ignore unsupported file extensions
        if not self.has_valid_extension(event.src_path):
            return

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

    def process_event_from_queue(self) -> None:
        try:
            event = self.queue.get_nowait()
        except asyncio.QueueEmpty:
            return

        if event.event_type == "created":
            self.process_created_event(event)
        else:
            self.process_moved_event(event)

    def process_created_event(self, event: FileSystemEvent) -> None:
        ...

    def process_moved_event(self, event: FileSystemEvent) -> None:
        ...
