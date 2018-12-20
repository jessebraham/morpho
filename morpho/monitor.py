# -*- coding: utf-8 -*-

import asyncio
import logging
import time

from typing import Generator

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class MorphoHandler(FileSystemEventHandler):
    def __init__(self, max_queue_size: int = 0) -> None:
        self.logger = logging.getLogger("morpho")
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(max_queue_size)  # type: asyncio.Queue

    def on_created(self, event) -> Generator:
        self.logger.info(event)
        yield from self.queue.put(event)

    def on_moved(self, event) -> Generator:
        self.logger.info(event)
        yield from self.queue.put(event)


class Monitor:
    def __init__(self) -> None:
        self.event_handler = MorphoHandler()
        self.observer = Observer()

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
