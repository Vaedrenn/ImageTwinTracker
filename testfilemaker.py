import os
import random
from PIL import Image

path = r"Tests\Dupe test"


# main driver function
def create_files():
    files = get_files(path)
    for f in files:
        random_resizer(f)


# get files
def get_files(src):
    filelist = []

    for root, dirs, files in os.walk(src):
        for file in files:
            # append the file name to the list
            filelist.append(os.path.join(root, file))
    """
    # print all the file names
    for name in filelist:
        print(name)
    """
    return filelist


# Generates duplicate images of the image with varying sizes
def random_resizer(file):
    arr = []
    for x in range(0, 10):
        x = random.randrange(600, 1920)
        arr.append(x)

    # print(arr)
    for x in arr:
        resize(file, x, 600)


# Resize a image and save it as a new file while keeping aspect ratio
# f_img: image file path
# width: width of image
# res: image quality in dpi
def resize(f_img, width, res):
    try:
        img = Image.open(f_img)

        # ignore gifs
        if not f_img.endswith("gif"):
            # Calculate resize percentage
            wpercent = (width / float(img.size[0]))

            # Calculate new high using above
            hsize = int((float(img.size[1]) * float(wpercent)))

            # Resize and save image
            print("resizing: ", f_img)
            img = img.resize((width, hsize), Image.ANTIALIAS)

            img.save(f_img + " dupe " + str(width) + ".jpg", dpi=(res, res))
            img.close()

    # Error handling
    except Exception as e:
        print(e)


# removes duplicates created for testing
def del_test():
    files = get_files(path)
    for x in files:
        if x.find("dupe") != -1:
            os.remove(x)


if __name__ == '__main__':
    del_test()
    create_files()
