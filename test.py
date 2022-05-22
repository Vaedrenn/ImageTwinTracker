import os
from datetime import time
from searchmse import create_tensor_list, mse_search

if __name__ == '__main__':
    # Test if the program creates all tensors
    root = r"tests\tensor test\test 1"
    tlist = create_tensor_list(root)

    if len(tlist) == 11:
        print("Test 1 passed")
    else:
        print("Test failed %s of 11 tensors created", len(tlist))

    # Test if the program accepts invalid files
    path = r"tests\tensor test\test 2"
    tlist = create_tensor_list(path)

    if len(tlist) == 11:
        print("Test 2 passed")
    else:
        print("Test failed %s of 11 tensors created", len(tlist))
        for img in tlist:
            print(img.path)

    # Test if mse search actually detects duplicates
    root = r"tests\Dupe test"
    testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
    print("MSE at threshold of 500")
    for folder in testfolders:
        print(folder)
        arr = create_tensor_list(folder)
        result = mse_search(arr, 500)
        for a in result:
            print(len(a), "of 11")
            print()

    # Should not detect any duplicates
    root = r"tests\dupe test 3"
    testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
    print("MSE at threshold of 500")
    for folder in testfolders:
        print(folder)
        arr = create_tensor_list(folder)
        result = mse_search(arr, 500)
        if result:
            print("failed")
        else:
            print("pass")
            print()

    # Should detect pairs
    root = r"tests\Mixed test"
    testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
    print("MSE at threshold of 500")
    for folder in testfolders:
        print(folder)
        arr = create_tensor_list(folder)
        result = mse_search(arr, 500)
        for a in result:
            print(len(a), "of 11")
            print()

    # Should detect 2 pairs
    root = r"tests\dupe test 2"
    testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
    print("MSE at threshold of 500")
    for folder in testfolders:
        print(folder)
        arr = create_tensor_list(folder)
        result = mse_search(arr, 500)
        for a in result:
            print(len(a), "of 2")
            print()
