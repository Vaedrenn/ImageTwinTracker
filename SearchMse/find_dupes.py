import imghdr
import multiprocessing
import os

import cv2
import numpy as np


class ImgData:
    def __init__(self, file_path, ratio, numpy_array):
        self.file_path = file_path
        self.ratio = ratio
        self.tensor = numpy_array

    def display_info(self):
        print("File Path:", self.file_path)
        print("Ratio:", self.ratio)
        print("NumPy Array:")
        print(self.numpy_array)


# read the image data and convert it into a tensor
def read_and_resize_image(file):
    # Open the image as a color image to prevent errors caused by grayscale images
    tensor = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
    if type(tensor) == np.ndarray:
        height, width, channels = tensor.shape
        if height > width:
            ratio = 'p'
        elif height < width:
            ratio = 'l'
        else:
            ratio = 's'
        #  check if it has been successfully converted to a numpy n-dimensional array, and has 3 layers at maximum.
        tensor = tensor[..., 0:3]
        # resize the image to speed up comparisons
        tensor = cv2.resize(tensor, dsize=(50, 50), interpolation=cv2.INTER_CUBIC)

    ret = ImgData(file, tensor, ratio)
    return ret


# MSE search each split of the tensor list
def fastsearch(arr, threshold=50):
    dupe_matrix = []
    for x in arr:
        temp = mse_search(x, threshold)
        for y in temp:
            dupe_matrix.append(y)
    return dupe_matrix


# Multiprocessing helper function
def process_file(file):
    # only process images don't process gifs
    if imghdr.what(file) and not imghdr.what(file) == "gif" and not imghdr.what(file) == "psd":
        return read_and_resize_image(file)
    else:
        return None


# creates a list of tensors for a given directory using multiprocessing
def create_img_list(root, threads, px_size=50):
    img_list = {
        'l': [],
        'w': [],
        'default': []
    }

    # create list of all files in directory
    folder_files = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in files]

    # create process pool
    with multiprocessing.Pool(processes=threads) as pool:
        # process files in parallel
        images = pool.map(process_file, folder_files)

    # collect tensors into the img_list
    for img in images:
        if img:
            ratio = img.ratio
            img_list.setdefault(ratio, []).append(img)

    return img_list


def mse(first, second):
    tensor1 = first.tensor
    tensor2 = second.tensor

    try:
        err = np.sum((tensor1.astype("float") - tensor2.astype("float")) ** 2)
        err /= float(tensor1.shape[0] * tensor1.shape[1])

        return err
    # Still want the program to continue, don't count the images as dupes and continue
    except ValueError:
        print("Value Error: ", first.path, second.path)
        return 1000000
    except AttributeError:
        print("Attribute Error: ", first.path, second.path)
        return 1000000


# # Searches for duplicates and removes them from the array when found
def mse_search(arr, threshold=20):
    dupe_matrix = []
    while len(arr) > 0:
        # reset i and dupes arr before each cycle, ignore the squiggly line
        i = 1
        dupes = []

        dupes.append(arr[0])
        # go through the tensors and find the mse
        while len(arr) >= 2 and i < len(arr):
            ratio = mse(arr[0], arr[i])
            # if the mse is less than the threshold add it to the bundle of dupes for this image
            if ratio < threshold:
                dupes.append(arr.pop(i))
                i = i - 1

            i = i + 1

        # If dupes has more than one object then put it into the return matrix
        if len(dupes) >= 2:
            dupe_matrix.append(dupes)
        arr.pop(0)

    return dupe_matrix
