#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class MorphoHandler(FileSystemEventHandler):
    def __init__(self):
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
