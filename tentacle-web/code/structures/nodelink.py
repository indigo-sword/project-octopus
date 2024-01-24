class NodeLink:
    def __init__(self, n1=None, n2=None, descr=""):
        self.n1 = n1          # node object
        self.n2 = n2          # node object
        # n1 and n2 order matters. n1 is the node that comes before n2.

        self.descr = descr    # string
        