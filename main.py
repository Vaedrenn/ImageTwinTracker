# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from searchmse import import_tensors, create_tensor_list, export_tensors, mse_search, mse_search_two


def driver():
    path = r"C:\Users\khei\Desktop\caedia5-likes-20220722_014512-20220823_171304-media"
    result = []
    # check cache

    # cache not found search for dupes in folder
    if not os.path.exists(r"more.pickle"):

        tlist = create_tensor_list(path)
        export_tensors(tlist, r"more.pickle")
        result = mse_search(tlist, 200)

    # cache found
    else:
        tlist = import_tensors(r"more.pickle")
        result = mse_search(tlist, 200)

    # export the results as html links for visual confirmation of dupes
    with open('dupes.html', 'w') as f:
        for x in result:
            for y in x:
                print(y.path)
                s = "<p><a target=\"_blank\" href = \" {} \"> {} </a></p>".format(y.path, y.path)
                f.write(s)
            print("")
            f.write("<p>-</p>")


def driver2():
    path = r"C:\Users\khei\Desktop\caedia5-likes-20220722_014512-20220823_171304-media"
    result = []
    # check cache

    # cache not found search for dupes in folder
    if not os.path.exists(r"more.pickle"):

        tlist = create_tensor_list(path)
        export_tensors(tlist, r"more.pickle")
        result = mse_search(tlist, 200)

    # cache found
    else:
        tlist = import_tensors(r"more.pickle")
        tlist2 = create_tensor_list(r"C:\Users\khei\Desktop\caedia5")
        result = mse_search_two(tlist2, tlist, 200)

    # export the results as html links for visual confirmation of dupes
    with open('dupes.html', 'w') as f:
        with open('dupes.html', 'w') as f:
            for x in result:
                for y in x:
                    print(y.path)
                    s = "<p><a target=\"_blank\" href = \" {} \"> {} </a></p>".format(y.path, y.path)
                    f.write(s)
                print("")
                f.write("<p>-</p>")



# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    driver()





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
