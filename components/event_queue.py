import threading
import queue

class EventQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self.run)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def enqueue(self, command):
        self.queue.put(command)

    def run(self):
        while True:
            command = self.queue.get()
            if command is None:
                break
            command.execute()

    def stop(self):
        self.queue.put(None)
        self.worker_thread.join()

