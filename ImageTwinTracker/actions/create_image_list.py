import logging
import os

import numpy as np
from PIL import Image
from PyQt5.QtCore import QRunnable, QThreadPool

logging.basicConfig(format="%(message)s", level=logging.INFO)


class ImgData:
    def __init__(self, file_path, ratio, numpy_array):
        self.file_path = file_path
        self.ratio = ratio
        self.tensor = numpy_array

    def display_path(self):
        print("File Path:", self.file_path)

    def display_info(self):
        print("File Path:", self.file_path)
        print("Ratio:", self.ratio)
        print("NumPy Array:")
        print(self.tensor)


class Runnable(QRunnable):
    def __init__(self, img_list, file):
        super().__init__()
        self.img_list = img_list
        self.file = file

    def run(self):
        img = read_and_resize_image(self.file)
        if img:
            if img.ratio == 'l':
                self.img_list[0].append(img)
            else:  # square images are rare dump in portrait
                self.img_list[1].append(img)


def create_image_list(main_widget):
    dir1 = main_widget.dir_line1.text()  # Get the text from the input field
    if not dir1:
        return

    threads = main_widget.preferences.get('Threads')
    if not threads:
        threads = 1
    landscape = []
    portrait = []
    img_list = (landscape, portrait)

    folder_files = [os.path.join(root, f) for root, dirs, files in os.walk(dir1) for f in files]
    pool = QThreadPool.globalInstance()

    ideal_thread_count = pool.maxThreadCount()
    if threads > pool.maxThreadCount():
        threads = pool.maxThreadCount()
    pool.setMaxThreadCount(threads)

    for file in folder_files:
        runnable = Runnable(img_list, file)
        pool.start(runnable)

    pool.waitForDone()
    pool.setMaxThreadCount(ideal_thread_count)  # reset to default max on exit
    return img_list


def read_and_resize_image(file):
    try:
        image = Image.open(file)
        string = f"Reading: {file}"
        logging.info(string)

        if image.mode != 'RGB':
            image = image.convert('RGB')
        width, height = image.size
        if height > width:
            ratio = 'p'
        else:
            ratio = 'l'
        image = image.resize((50, 50), Image.LANCZOS)
        image_array = np.array(image)
        return ImgData(file, ratio, image_array)
    except (IOError, OSError):
        string = f"Not an image: {file}"
        logging.info(string)
        return None
    except Image.DecompressionBombError:
        string = f"Skipping absurdly large image due to decompression bomb error :{file}"
        logging.info(string)
        return None
