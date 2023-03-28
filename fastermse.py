import os
import numpy as np
import cv2
import imghdr
import multiprocessing
import searchmse
from tcontainer import tcontainer


# creates a list of tensors for a given directory
def create_tensor_list(root, px_size=50):
    landscape = []
    portrait = []
    square = []
    tensor_list = (landscape, portrait, square)

    # create list of all files in directory
    folder_files = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in files]
    for file in folder_files:
        # only process images don't process gifs
        if imghdr.what(file) and not imghdr.what(file) == "gif" and not imghdr.what(file) == "psd":
            tensor = create_tensor(file)
            if tensor.ratio == 'l':
                tensor_list[0].append(tensor)
            elif tensor.ratio == 'w':
                tensor_list[1].append(tensor)
            else:
                tensor_list[2].append(tensor)
    return tensor_list


# read the image data and convert it into a tensor
def create_tensor(file):
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

    ret = tcontainer(file, tensor, ratio)
    return ret


# MSE search each split of the tensor list
def fastsearch(arr, threshold=50):
    dupe_matrix = []
    for x in arr:
        temp = searchmse.mse_search(x, threshold)
        for y in temp:
            dupe_matrix.append(y)
    return dupe_matrix


# Multiprocessing helper function
def process_file(file):
    # only process images don't process gifs
    if imghdr.what(file) and not imghdr.what(file) == "gif" and not imghdr.what(file) == "psd":
        return create_tensor(file)
    else:
        return None


# creates a list of tensors for a given directory using multiprocessing
def create_tensor_list_multiproc(root, px_size=50, num_processes=4):
    landscape = []
    portrait = []
    square = []
    tensor_list = (landscape, portrait, square)

    # create list of all files in directory
    folder_files = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in files]

    # create process pool
    with multiprocessing.Pool(processes=num_processes) as pool:
        # process files in parallel
        tensors = pool.map(process_file, folder_files)

    # collect tensors into the tensor_list
    for tensor in tensors:
        if tensor:
            if tensor.ratio == 'l':
                tensor_list[0].append(tensor)
            elif tensor.ratio == 'w':
                tensor_list[1].append(tensor)
            else:
                tensor_list[2].append(tensor)

    return tensor_list
