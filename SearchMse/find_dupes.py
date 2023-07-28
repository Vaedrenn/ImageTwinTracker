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

    def display_path(self):
        print("File Path:", self.file_path)

    def display_info(self):
        print("File Path:", self.file_path)
        print("Ratio:", self.ratio)
        print("NumPy Array:")
        print(self.tensor)


# creates a list of tensors for a given directory using multiprocessing
def create_img_list(root, px_size=50, num_processes=4):
    landscape = []
    portrait = []
    img_list = (landscape, portrait)

    # create list of all files in directory
    folder_files = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in files]

    # create process pool
    with multiprocessing.Pool(processes=num_processes) as pool:
        # process files in parallel
        tensors = pool.map(__process_file, folder_files)

    # collect tensors into the tensor_list
    for img in tensors:
        if img:
            if img.ratio == 'l':
                img_list[0].append(img)
            else:  # square images are rare dump in portrait
                img_list[1].append(img)

    return img_list


# Multiprocessing helper function
def __process_file(file):
    # only process images don't process gifs
    if imghdr.what(file) and not imghdr.what(file) == "gif" and not imghdr.what(file) == "psd":
        return read_and_resize_image(file)
    else:
        return None


# read the image data and convert it into a tensor
def read_and_resize_image(file):
    # Open the image as a color image to prevent errors caused by grayscale images
    image = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is not None and type(image) == np.ndarray:
        height, width, channels = image.shape
        if height > width:
            ratio = 'p'
        else:
            ratio = 'l'
        #  check if it has been successfully converted to a numpy n-dimensional array, and has 3 layers at maximum.
        image = image[..., 0:3]
        # resize the image to speed up comparisons
        image = cv2.resize(image, dsize=(50, 50), interpolation=cv2.INTER_CUBIC)
    else:
        return
    ret = ImgData(file, ratio, image)
    return ret


# MSE search each split of the tensor list
def find_dupes(img_list, threads, threshold=200):
    dupe_matrix = []

    # if multiprocessing is enabled
    if threads >= 2:
        with multiprocessing.Pool(processes=2) as pool:
            # Todo: make it pass in threshold
            ret_matrix = pool.starmap(mse_search, [(x, threshold) for x in img_list])
            for sublist in ret_matrix:  # 2
                for i in sublist:  #
                    dupe_matrix.append(i)
        return dupe_matrix

    for x in img_list:  # does this twice, once for landscapes and once for portraits
        temp = mse_search(x, threshold)
        dupe_matrix.extend(temp)  # Extend instead of appending each sublist
    return dupe_matrix


def __mse(first, second):
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
def mse_search(arr, threshold=50):
    dupe_matrix = []
    while len(arr) > 0:
        # reset i and dupes arr before each cycle, ignore the squiggly line
        i = 1
        dupes = []

        dupes.append(arr[0])
        # go through the tensors and find the mse
        while len(arr) >= 2 and i < len(arr):
            ratio = __mse(arr[0], arr[i])
            # print(arr[0].display_path(), arr[1].display_path(), "Ratio: ", ratio)
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