import multiprocessing
from multiprocessing import Process, Queue, Pipe
import os
import numpy as np
import time

class SaveImageCommand:
    def __init__(self):
        self.save_counter = 1
        self.save_queue = Queue()
        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=self._save_image_process, args=(self.child_conn,), daemon=True)
        self.process.start()
        self.child_conn.close()

    def execute(self, model):
        """
        Enqueue a save request with the model data.
        """
        if model.pixels.size == 0:
            self.parent_conn.send(("error", "Brak wczytanego obrazu do zapisania."))
            return
        self.save_queue.put({
            "format": model.format,
            "width": model.width,
            "height": model.height,
            "maxval": model.maxval,
            "pixels": model.pixels.copy(),
            "counter": self.save_counter
        })

    def _save_image_process(self, conn):
        while True:
            try:
                save_request = self.save_queue.get()
                if save_request is None:
                    break

                format_ = save_request["format"]
                width = save_request["width"]
                height = save_request["height"]
                maxval = save_request["maxval"]
                pixels = save_request["pixels"]
                counter = save_request["counter"]

                save_dir = "save_images"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    print(f"Utworzono katalog: {save_dir}")

                while True:
                    filename = f"image({counter}).ppm"
                    filepath = os.path.join(save_dir, filename)
                    if not os.path.exists(filepath):
                        break
                    counter += 1

                save_request["counter"] = counter

                try:
                    with open(filepath, 'wb') as f:
                        f.write(f"{format_}\n".encode('ascii'))
                        f.write(f"{width} {height}\n".encode('ascii'))
                        if format_ in ['P2', 'P3', 'P5', 'P6']:
                            f.write(f"{maxval}\n".encode('ascii'))

                        if format_ in ['P3', 'P6']:
                            if format_ == 'P3':
                                pixel_data = ' '.join(map(str, pixels.flatten()))
                                f.write(pixel_data.encode('ascii'))
                            elif format_ == 'P6':
                                if pixels.dtype == np.uint8:
                                    f.write(pixels.tobytes())
                                elif pixels.dtype == np.uint16:
                                    f.write(pixels.byteswap().tobytes())
                        elif format_ in ['P2', 'P5']:
                            if format_ == 'P2':
                                pixel_data = ' '.join(map(str, pixels.flatten()))
                                f.write(pixel_data.encode('ascii'))
                            elif format_ == 'P5':
                                if pixels.dtype == np.uint8:
                                    f.write(pixels.tobytes())
                                elif pixels.dtype == np.uint16:
                                    f.write(pixels.byteswap().tobytes())
                        elif format_ in ['P1', 'P4']:
                            if format_ == 'P1':
                                pixel_data = ' '.join(map(str, pixels.flatten()))
                                f.write(pixel_data.encode('ascii'))
                            elif format_ == 'P4':
                                packed_bits = np.packbits(pixels.flatten())
                                f.write(packed_bits.tobytes())
                    print(f"Obraz zapisany jako {filepath}")
                    conn.send(("success", f"Obraz zapisany jako {filename}"))
                    self.save_counter += 1
                except Exception as e:
                    print(f"Błąd podczas zapisywania obrazu: {e}")
                    conn.send(("error", f"Błąd podczas zapisywania obrazu: {e}"))
            except EOFError:
                break

    def check_status(self):
        """
        Sprawdź, czy proces zapisu wysłał jakieś wiadomości.
        """
        if self.parent_conn.poll():
            status, message = self.parent_conn.recv()
            return status, message
        return None, None

    def terminate(self):
        """
        Zakończ proces zapisu.
        """
        self.save_queue.put(None)
        self.process.join()
        self.parent_conn.close()

