import threading
import numpy as np
import re

class PPMImageModel:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.maxval = 255  
        self.pixels = np.array([])
        self.format = ''
        self.image_ready = threading.Event()
        self.lock = threading.Lock()

    def load_ppm(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                magic_number = f.readline().strip()
                if not magic_number:
                    raise ValueError("Pusty plik.")
                self.format = magic_number.decode('ascii')
                if self.format not in ['P1','P2','P3','P4','P5','P6']:
                    raise ValueError("Nieobsługiwany format PPM.")

                def read_token():
                    while True:
                        byte = f.read(1)
                        if not byte:
                            raise ValueError("Nieoczekiwany koniec pliku podczas odczytu nagłówka.")
                        if byte == b'#':
                            f.readline()
                            continue
                        if byte in b' \t\r\n':
                            continue
                        token = b''
                        while byte not in b' \t\r\n' and byte != b'':
                            token += byte
                            byte = f.read(1)
                            if not byte:
                                break
                        return token.decode('ascii')

                self.width = int(read_token())
                self.height = int(read_token())
                if self.format in ['P2','P3','P5','P6']:
                    self.maxval = int(read_token())
                else:
                    self.maxval = 1 

                print(self.width)
                print('with')
                print(self.height)
                print("heiught")
                print(self.maxval)
                print("maxval")

                if self.maxval < 256:
                    dtype = np.uint8
                elif self.maxval < 65536:
                    dtype = np.uint16
                else:
                    raise ValueError("maxval jest zbyt duży.")

                if self.format == 'P3':
                    remaining_content = f.read().decode('iso-8859-2')
                    remaining_content = re.sub(r'#.*', '', remaining_content)
                    tokens = remaining_content.split()
                    expected_pixels = self.width * self.height * 3
                    actual_pixels = len(tokens)
                    print(actual_pixels)
                    if actual_pixels < expected_pixels:
                        raise ValueError(f"Za mało danych pikseli. Oczekiwano {expected_pixels}, otrzymano {actual_pixels}.")
                    pixel_data = np.array(tokens[:expected_pixels], dtype=dtype).reshape((self.height, self.width, 3))
                elif self.format == 'P6':
                    expected_size = self.width * self.height * 3 * (2 if dtype == np.uint16 else 1)
                    pixel_bytes = f.read(expected_size)
                    actual_size = len(pixel_bytes)
                    print(actual_size)
                    if actual_size < expected_size:
                        raise ValueError(f"Za mało danych pikseli. Oczekiwano {expected_size} bajtów, otrzymano {actual_size} bajtów.")
                    pixel_data = np.frombuffer(pixel_bytes, dtype=dtype).reshape((self.height, self.width, 3))
                elif self.format == 'P2':
                    remaining_content = f.read().decode('iso-8859-2')
                    remaining_content = re.sub(r'#.*', '', remaining_content)
                    tokens = remaining_content.split()
                    expected_pixels = self.width * self.height
                    actual_pixels = len(tokens)
                    print(actual_pixels)
                    if actual_pixels < expected_pixels:
                        raise ValueError(f"Za mało danych pikseli. Oczekiwano {expected_pixels}, otrzymano {actual_pixels}.")
                    pixel_data = np.array(tokens[:expected_pixels], dtype=dtype).reshape((self.height, self.width))
                elif self.format == 'P5':
                    expected_size = self.width * self.height * (2 if dtype == np.uint16 else 1)
                    pixel_bytes = f.read(expected_size)
                    actual_size = len(pixel_bytes)
                    print(actual_size)
                    if actual_size < expected_size:
                        raise ValueError(f"Za mało danych pikseli. Oczekiwano {expected_size} bajtów, otrzymano {actual_size} bajtów.")
                    pixel_data = np.frombuffer(pixel_bytes, dtype=dtype).reshape((self.height, self.width))
                elif self.format == 'P1':
                    remaining_content = f.read().decode('iso-8859-2')
                    remaining_content = re.sub(r'#.*', '', remaining_content)
                    tokens = remaining_content.split()
                    expected_pixels = self.width * self.height
                    actual_pixels = len(tokens)
                    print(actual_pixels)
                    if actual_pixels < expected_pixels:
                        raise ValueError(f"Za mało danych pikseli. Oczekiwano {expected_pixels}, otrzymano {actual_pixels}.")
                    pixel_data = np.array(tokens[:expected_pixels], dtype=np.uint8).reshape((self.height, self.width))
                elif self.format == 'P4':
                    row_bytes = (self.width + 7) // 8
                    expected_size = row_bytes * self.height
                    pixel_bytes = f.read(expected_size)
                    actual_size = len(pixel_bytes)
                    print(actual_size)
                    if actual_size < expected_size:
                        raise ValueError(f"Za mało danych pikseli. Oczekiwano {expected_size} bajtów, otrzymano {actual_size} bajtów.")
                    bits = np.unpackbits(np.frombuffer(pixel_bytes, dtype=np.uint8))
                    bits = bits[:self.width * self.height]
                    pixel_data = bits.reshape((self.height, self.width))
                else:
                    raise ValueError("Nieobsługiwany format PPM.")

                with self.lock:
                    self.pixels = pixel_data
                    self.image_ready.set()
        except Exception as e:
            print(f"Błąd podczas wczytywania PPM: {e}")
            raise

    def get_image_data(self):
        with self.lock:
            return self.pixels.copy() if self.pixels.size else None

