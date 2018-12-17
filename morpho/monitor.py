# -*- coding: utf-8 -*-

import logging
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class MorphoHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self.logger = logging.getLogger("morpho")

    def on_created(self, event) -> None:
        self.logger.info(event)

    def on_moved(self, event) -> None:
        self.logger.info(event)


class Monitor:
    def __init__(self) -> None:
        self.observer = Observer()
        self.event_handler = MorphoHandler()

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
