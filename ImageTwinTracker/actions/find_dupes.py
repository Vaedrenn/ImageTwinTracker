import numpy as np
from PyQt5.QtCore import QRunnable, QThreadPool


class Runnable(QRunnable):
    def __init__(self, img_list, dupe_matrix, threshold):
        super().__init__()
        self.img_list = img_list
        self.dupe_matrix = dupe_matrix
        self.threshold = threshold

    def run(self):
        arr = mse_search(self.img_list, self.threshold)
        for x in arr:
            self.dupe_matrix.append(x)


# MSE search each split of the tensor list
def find_dupes(img_list, threshold=200):
    dupe_matrix = []

    if not img_list:
        return dupe_matrix

    pool = QThreadPool.globalInstance()
    for x in range(2):
        runnable = Runnable(img_list[x], dupe_matrix, threshold)
        pool.start(runnable)

    pool.waitForDone()
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
            arr[0].display_path()
            arr[i].display_path()
            print("Ratio: ", ratio)
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
