# Container Object to hold file path and the tensor
class tcontainer:
    def __init__(self, p, t):
        self.path = p
        self.tensor = t

    def __print__(self):
        print(self.path)
