import os
from unittest import TestCase

import searchmse


class TestCreate(TestCase):

    # Test if exactly 11 objects are created
    def test_len(self):
        root = r"tests\tensor test\test 1"
        tlist = searchmse.create_tensor_list(root)
        self.assertEqual(len(tlist), 11)

    # Test if the program accepts invalid files
    def test_valid(self):
        root = r"tests\tensor test\test 2"
        tlist = searchmse.create_tensor_list(root)
        self.assertEqual(len(tlist), 11)


class TestSearch(TestCase):
    # Test if mse search actually detects duplicates
    def test_dupes(self, threshold=500, root=r"tests\Dupe test"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 8)
        for folder in testfolders:
            arr = searchmse.create_tensor_list(folder)
            if not arr:
                self.fail()
            result = searchmse.mse_search(arr, threshold)
            if not result:
                self.fail()
            for a in result:
                self.assertEqual(len(a), 11)

    # Should not find any duplicates
    def test_dupes_false(self, threshold=500, root=r"tests\dupe test 2"):

        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        if not testfolders:
            self.fail()
        for folder in testfolders:
            arr = searchmse.create_tensor_list(folder)
            if not arr:
                self.fail()
            result = searchmse.mse_search(arr, threshold)
            for a in result:
                self.assertEqual(len(a), None)

    # Test mixed folder of dupes and none dupes
    def test_dupe_mixed(self, threshold=500, root=r"tests\dupe test 3"):

        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 2)
        for folder in testfolders:
            arr = searchmse.create_tensor_list(folder)
            result = searchmse.mse_search(arr, threshold)
            self.assertEqual(len(result), 2)
            for a in result:
                self.assertEqual(len(a), 2)


class TestImportExport(TestCase):
    # Test if the pickle file is created
    def test_export_tensors(self, path=r"Tests\Dupe test"):
        tlist = searchmse.create_tensor_list(path)
        searchmse.export_tensors(tlist)
        files = os.listdir()
        self.assertEqual(files.count("tensors.pickle"), 1)

    # Test if importing the pickle file works
    def test_import_tensors(self):
        tlist = searchmse.import_tensors()
        # Successful import?
        if not tlist:
            self.fail()
        # Can we use it?
        result = searchmse.mse_search(tlist, 1000)
        if not result:
            self.fail()
        # Is it accurate?
        self.assertEqual(len(result), 8)
        for r in result:
            self.assertEqual(len(r), 11)
