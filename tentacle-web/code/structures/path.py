class PathId:
    def __init__(self):
        self.id = 0            # create an ID

    def get(self):
        return self.id
    
class PathDescription:
    def __init__(self, descr=""):
        self.descr = descr    # string

    def set(self, descr):
        self.descr = descr

    def get(self):
        return self.descr

# paths WILL need to be stored in a DB.
class Path:
    def __init__(self):
        self.id = PathId()
        self.node_sequence = []
        self.description = PathDescription()