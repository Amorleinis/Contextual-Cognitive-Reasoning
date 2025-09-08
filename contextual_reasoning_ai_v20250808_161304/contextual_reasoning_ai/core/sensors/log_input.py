import os
import time

class LogFileSensor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.last_position = 0

    def stream(self):
        while True:
            if not os.path.exists(self.filepath):
                time.sleep(1)
                continue
            with open(self.filepath, 'r') as f:
                f.seek(self.last_position)
                lines = f.readlines()
                self.last_position = f.tell()
                for line in lines:
                    yield line.strip()
            time.sleep(1)
