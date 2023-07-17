import send2trash

def deletefiles(files):
    for file in files:
        send2trash.send2trash(file)

    return 0