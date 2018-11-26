import time
from concurrent.futures import ThreadPoolExecutor

from ..file_watch import BaseWatchHandler
from ..utils.time_utility import tsnow
from ..utils.mail_utility import send_email


executor = ThreadPoolExecutor(max_workers=3)


class EmailHandler(BaseWatchHandler):
    
    def __init__(self):
        self.buffer = []
        self.last_send_time = tsnow()
        self.send_interval = 60

    def should_flush(self):
        now = tsnow()
        should_flush = (now - self.last_send_time) > self.send_interval
        return should_flush and self.buffer

    def flush(self):
        buffers = self.buffer
        self.buffer = []
        self.last_send_time = tsnow()
        executor.emit(send_email, host, port, username, password, subject, ''.join(buffers))

    def process(self, content):
        self.buffer.extend(content)
        if self.should_flush():
            self.flush()
        
