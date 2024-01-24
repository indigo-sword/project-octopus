class Node:
    def __init__(self):
        self.previous = []      # array of NodeLink structures
        self.next = []          # array of NodeLink structures
        self.level = None       # gotta see how this works
        self.description = ""   # string -- not sure if necessary
        self.owner = None       # user object
        self.playcount = 0      # int
        self.ID = None          # ?

class NodeLink:
    def __init__(self):
        self.n1 = None          # node object
        self.n2 = None          # node object
        self.descr = ""         # string