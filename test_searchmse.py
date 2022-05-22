import os
from unittest import TestCase

import searchmse
from searchmse import create_tensor_list, mse_search


class Test_create(TestCase):

    # Test if exactly 11 objects are created
    def test_len(self):
        root = r"tests\tensor test\test 1"
        tlist = create_tensor_list(root)
        self.assertEqual(len(tlist), 11)

    # Test if the program accepts invalid files
    def test_valid(self):
        root = r"tests\tensor test\test 2"
        tlist = create_tensor_list(root)
        self.assertEqual(len(tlist), 11)


class Test_search(TestCase):
    # Test if mse search actually detects duplicates
    def test_dupes(self, threshold=500):
        root = r"tests\Dupe test"
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 8)
        for folder in testfolders:
            arr = create_tensor_list(folder)
            if not arr:
                self.fail()
            result = mse_search(arr, threshold)
            if not result:
                self.fail()
            for a in result:
                self.assertEqual(len(a), 11)

    # Should not find any duplicates
    def test_dupes_false(self, threshold=500):
        root = r"tests\dupe test 2"
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        if not testfolders:
            self.fail()
        for folder in testfolders:
            arr = create_tensor_list(folder)
            if not arr:
                self.fail()
            result = mse_search(arr, threshold)
            for a in result:
                self.assertEqual(len(a), None)

    # Test mixed folder of dupes and none dupes
    def test_dupe_mixed(self, threshold=500):
        root = r"tests\dupe test 3"
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 2)
        for folder in testfolders:
            arr = create_tensor_list(folder)
            result = mse_search(arr, 500)
            self.assertEqual(len(result), 2)
            for a in result:
                self.assertEqual(len(a), 2)
