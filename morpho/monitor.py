# -*- coding: utf-8 -*-

import asyncio
import logging
import time

from typing import Generator

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class MorphoHandler(FileSystemEventHandler):
    def __init__(self, logger: logging.Logger, queue: asyncio.Queue) -> None:
        self.logger = logger
        self.queue = queue

    def on_created(self, event) -> Generator:
        self.logger.info(event)
        yield from self.queue.put(event)

    def on_moved(self, event) -> Generator:
        self.logger.info(event)
        yield from self.queue.put(event)

class MorphoWorker:
    def __init__(self, logger: logging.Logger, queue: asyncio.Queue) -> None:
        self.logger = logger
        self.queue = queue


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
