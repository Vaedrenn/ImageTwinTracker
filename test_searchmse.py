import os
from unittest import TestCase

import fastermse
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
        # Each folder has two pairs of duplicate images
        for folder in testfolders:
            arr = searchmse.create_tensor_list(folder)
            result = searchmse.mse_search(arr, threshold)
            # Are there two groups of duplicate images?
            self.assertEqual(len(result), 2)
            # Are there only two images per?
            for a in result:
                self.assertEqual(len(a), 2)
            for x in result:
                for y in x:
                    print(y.path)


class TestSearch2(TestCase):
    # Test false detection
    def test_false(self):
        src = r"Tests\Dupe test\Checkers"
        dst = r"Tests\Dupe test\simple black"
        srclist = searchmse.create_tensor_list(src)
        dstlist = searchmse.create_tensor_list(dst)

        arr = searchmse.mse_search_two(srclist, dstlist, 500)
        if arr:
            self.fail()

    # Test if it returns the 3 dupes
    def test_dupe_test(self):
        src = r"Tests\Two folders\src"
        dst = r"Tests\Two folders\dst"

        srclist = searchmse.create_tensor_list(src)
        dstlist = searchmse.create_tensor_list(dst)
        arr = searchmse.mse_search_two(srclist, dstlist, 500)

        self.assertEqual(len(arr), 3)


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

        if not tlist:
            self.fail()

        result = searchmse.mse_search(tlist, 500)
        if not result:
            self.fail()

        self.assertEqual(len(result), 8)
        for r in result:
            self.assertEqual(len(r), 11)

    # test import with the mixed test
    def test_import_tensors2(self, path=r"Tests\dupe test 3\test 2"):
        tlist = searchmse.create_tensor_list(path)
        searchmse.export_tensors(tlist, "tensors2.pickle")

        tlist = []
        tlist = searchmse.import_tensors(r"tensors2.pickle")
        result = searchmse.mse_search(tlist, 500)
        if not result:
            self.fail()

        self.assertEqual(len(result), 2)
        for r in result:
            self.assertEqual(len(r), 2)


class TestFasterSearch(TestCase):

    # Test mixed folder of dupes and none dupes
    def test_dupe_mixed(self, threshold=500, root=r"tests\dupe test 3"):

        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 2)
        # Each folder has two pairs of duplicate images
        for folder in testfolders:
            arr = fastermse.create_tensor_list(folder)
            result = fastermse.fastsearch(arr, threshold)

            # Are there two groups of duplicate images?
            self.assertEqual(len(result), 2)
            # Are there only two images per?
            for a in result:
                self.assertEqual(len(a), 2)


class TestSearchmp(TestCase):
    # Test if mse search actually detects duplicates
    def test_dupes(self, threshold=500, root=r"tests\Dupe test"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 8)

        for folder in testfolders:
            arr = fastermse.create_tensor_list_multiproc(folder)
            if not arr:
                self.fail()

            result = fastermse.fastsearch(arr, threshold)
            if not result:
                self.fail()

            for a in result:
                print(a[0].path)
                self.assertEqual(len(a), 11)

    # Should not find any duplicates
    def test_dupes_false(self, threshold=500, root=r"tests\dupe test 2"):
        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        if not testfolders:
            self.fail()

        for folder in testfolders:
            arr = fastermse.create_tensor_list_multiproc(folder)
            if not arr:
                self.fail()

            result = fastermse.fastsearch(arr, threshold)
            for a in result:
                self.assertEqual(len(a), None)

    # Test mixed folder of dupes and none dupes
    def test_dupe_mixed(self, threshold=500, root=r"tests\dupe test 3"):

        testfolders = [os.path.join(root, f) for root, dirs, files in os.walk(root) for f in dirs]
        self.assertEqual(len(testfolders), 2)
        # Each folder has two pairs of duplicate images
        for folder in testfolders:
            arr = fastermse.create_tensor_list_multiproc(folder)
            result = fastermse.fastsearch(arr, threshold)

            # Are there two groups of duplicate images?
            self.assertEqual(len(result), 2)
            # Are there only two images per?
            for a in result:
                self.assertEqual(len(a), 2)


if __name__ == '__main__':
    TestCreate()
    TestSearch()
    TestImportExport()
    TestFasterSearch()
    TestSearchmp()
