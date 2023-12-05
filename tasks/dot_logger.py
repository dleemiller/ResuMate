import logging
import threading
import time


class DotLogger:
    def __init__(self, logger: logging.Logger, timeout: int = 10):
        self.logger = logger
        self.stop_event = threading.Event()
        self.timeout = timeout

    def log_dot(self, interval: float = 0.2):
        counter = 0
        while not self.stop_event.is_set():
            time.sleep(interval)
            if counter >= self.timeout:
                self.logger.info(f"Running... {time.time() - self.start_time:.1f}s")
                counter = 0
            else:
                counter += interval

    def start_logging(self):
        self.thread = threading.Thread(target=self.log_dot)
        self.thread.start()
        self.start_time = time.time()

    def stop_logging(self):
        self.stop_event.set()
        self.thread.join()

    def __enter__(self):
        self.start_logging()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_logging()
