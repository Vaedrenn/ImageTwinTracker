import os
from unittest import TestCase

import numpy as np

from SearchMse.find_dupes import create_img_list, find_dupes, ImgData, read_and_resize_image, __mse


class TestCreate(TestCase):

    # Test if exactly 11 objects are created
    def test_len(self):
        root = r"Dupe test/Complex 3"
        if not root:
            self.fail("Directory not found")
        img_list = create_img_list(root, 2)
        landscape = img_list[0]
        portrait = img_list[1]

        self.assertEqual(len(landscape), 11)
        self.assertEqual(len(set(landscape)), 11)
        """
        print("landscape")
        for img in landscape:
            img.display_path()
        print("portrait")
        for img in portrait:
            img.display_path()
        """

    # Test if the program accepts invalid files
    def test_valid(self):
        root = r"Tensor test/test 2"
        if not root:
            self.fail("Directory not found")
        img_list = create_img_list(root, 2)
        landscape = img_list[0]
        portrait = img_list[1]
        dud = r"Tensor test/test 2/dud.txt"

        self.assertFalse(dud in landscape)
        self.assertFalse(dud in portrait)


class TestSearch(TestCase):
    # Test if mse search actually detects duplicates
    def test_dupes(self, threshold=500, root=r"Dupe test"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 8)

        for folder in testfolders:
            arr = create_img_list(folder)
            if not arr:
                self.fail()

            result = find_dupes(arr, 4, threshold)
            if not result:
                self.fail()

            for a in result:
                self.assertEqual(len(a), 11)

    # Should not find any duplicates
    def test_dupes_false(self, threshold=500, root=r"dupe test 2"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        if not testfolders:
            self.fail()

        for folder in testfolders:
            arr = create_img_list(folder)
            if not arr:
                self.fail()

            result = find_dupes(arr, threshold)
            for a in result:
                self.assertEqual(len(a), None)

    # Test mixed folder of dupes and none dupes
    def test_dupe_mixed1c(self, threshold=200, root=r"dupe test 3/test 1"):

        # concurrent testing
        test1 = create_img_list(root)
        result1 = find_dupes(test1, 1, threshold)
        if self.assertEqual(len(result1),2):
            for dupes in result1:
                for a in dupes:
                    a.display_path()
        else:
            for a in result1:
                self.assertEqual(len(a),2)
                self.assertEqual(len(set(a)), 2)

    def test_dupe_mixed2c(self, threshold=200, root=r"Dupe test 3/Test 2"):

        test2 = create_img_list(root)
        result2 = find_dupes(test2, 1, threshold)
        if self.assertEqual(len(result2), 3):
            for dupes in result2:
                for a in dupes:
                    a.display_path()
        else:
            for a in result2:
                self.assertEqual(len(a), 2)
                self.assertEqual(len(set(a)), 2)

    def test_dupe_mixed1p(self, threshold=200, root=r"dupe test 3/Test 1"):
        # parallel testing
        test1 = create_img_list(root)
        result1 = find_dupes(test1, 2, threshold)
        if self.assertEqual(len(result1),2):
            for dupes in result1:
                for a in dupes:
                    a.display_path()
        else:
            for a in result1:
                self.assertEqual(len(a),2)
                self.assertEqual(len(set(a)), 2)

    def test_dupe_mixed2p(self, threshold=200, root=r"dupe test 3/Test 2"):

        test2 = create_img_list(root)
        result2 = find_dupes(test2, 2, threshold)
        if self.assertEqual(len(result2), 3):
            for dupes in result2:
                for a in dupes:
                    a.display_path()
        else:
            for a in result2:
                self.assertEqual(len(a), 2)
                self.assertEqual(len(set(a)), 2)


if __name__ == '__main__':
    TestCreate()
    TestSearch()