class Node:
    def __init__(self):
        self.previous = set()       # set of NodeLink structures
        self.next = set()           # set of NodeLink structures
        self.level = None           # gotta see how this works
        self.description = ""       # string -- not sure if necessary
        self.owner = None           # user object
        self.playcount = 0          # int
        self.ID = None              # ?

    # link to next node by doing node1.link_next(node2, "some action that gets taken")
    def link_next(self, node, descr):
        # create a Nodelink object
        l = NodeLink(self, node, descr)

        # add the link to both nodes
        self.next.add(l)
        node.previous.add(l)

    # link to previous node by doing node1.link_prev(node2, "some action that gets taken")
    def link_prev(self, node, descr):
        # create a Nodelink object
        l = NodeLink(node, self, descr)

        # add the link to both nodes
        self.previous.add(l)
        node.next.add(l)

class NodeLink:
    def __init__(self, n1=None, n2=None, descr=""):
        self.n1 = n1          # node object
        self.n2 = n2          # node object
        # n1 and n2 order matters. n1 is the node that comes before n2.

        self.descr = descr    # string