import multiprocessing
from multiprocessing import Process, Pipe
from components.choose_file import choose_file
from model.ppm_image_model import PPMImageModel
import time
import threading
import queue

class LoadImageCommand:
    def __init__(self, model):
        self.model = model
        self.process = None
        self.parent_conn = None
        self.child_conn = None
        self.file_queue = queue.Queue()
        self.is_loading = False

    def execute(self):
        thread = threading.Thread(target=self._choose_file_thread, daemon=True)
        thread.start()

    def _choose_file_thread(self):
        file_path = choose_file()
        if file_path:
            self.file_queue.put(file_path)

    def process_queue(self):
        if not self.is_loading and not self.file_queue.empty():
            try:
                file_path = self.file_queue.get_nowait()
                with self.model.lock:
                    self.model.width = 0
                    self.model.height = 0
                    self.model.maxval = 255
                    self.model.pixels = []
                    self.model.format = ''
                    self.model.image_ready.clear()
                    self.model.loading_time = None

                self.parent_conn, self.child_conn = Pipe()

                self.process = Process(target=self.load_image, args=(self.child_conn, file_path))
                self.process.start()
                self.child_conn.close()

                self.is_loading = True
            except queue.Empty:
                pass

    def load_image(self, conn, file_path):
        try:
            model = PPMImageModel()
            start_time = time.time()
            model.load_ppm(file_path)
            end_time = time.time()
            print(f"Czas wczytywania: {end_time - start_time:.2f} sekundy")
            loading_time = end_time - start_time
            conn.send((model.width, model.height, model.maxval, model.format, model.pixels, loading_time))
        except Exception as e:
            conn.send(('exception', str(e)))
        finally:
            conn.close()

    def check_process(self):
        self.process_queue()

        if self.process is not None:
            if self.parent_conn.poll():
                data = self.parent_conn.recv()
                if data[0] == 'exception':
                    print('Exception in image loading process:')
                    print(data[1])
                    self.model.image_ready.set()
                else:
                    with self.model.lock:
                        self.model.width, self.model.height, self.model.maxval, self.model.format, self.model.pixels, self.model.loading_time = data
                        print('Image data received in main process')
                        self.model.image_ready.set()
                self.process.join()
                self.process = None
                self.is_loading = False 
            elif not self.process.is_alive():
                self.process.join()
                self.process = None
                self.is_loading = False

