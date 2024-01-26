from level import Level
from user import User

# All of this code is not database-ready yet. 
# we need to create code to initiate empty guys.
# we need to create code to load, save, update and delete them to the database.

# OR: we could use an ORM like SQLAlchemy to do this for us, so the objects will be
# stored and we don't have to worry about it.

class NodeId:
    def __init__(self):
        self.id = 0            # create an ID

    def get(self):
        return self.id

class NodeDescription:
    def __init__(self, descr: str=""):
        self.descr = descr    # string

    def set(self, descr):
        self.descr = descr

    def get(self):
        return self.descr

class NodeLink:
    def __init__(self, n=NodeId(), descr=NodeDescription()):
        self.node = n                 
        self.descr = descr 
    
    def get_node(self):
        return self.node
    
    def get_description(self):
        return self.descr.get()

class Node:
    def __init__(self, level: Level, description: NodeDescription, user: User):
        self.level = level                   
        self.description = description   
        self.user = user                     
        self.id = NodeId()

        # attributes that will change over time. we will need to model their functions
        # so that they can deal with concurrent access.

        # or maybe we can leave it to the database / API to deal with concurrent access
        # because we will save them in a DB, right?
        
        self.previous = set()                
        self.next = set()                 
        self.playcount = 0
        self.rating = 0

    def link_next(self, node: 'Node', description: NodeDescription):
        ''' link to next node '''
        if node == self:
            raise Exception("Cannot link node to itself")
        
        self.next.add(NodeLink(node.id, description))
        node.previous.add(NodeLink(self.id, description))

    def link_previous(self, node: 'Node', description: NodeDescription):
        ''' link to next node '''
        if node == self:
            raise Exception("Cannot link node to itself")
        
        self.previous.add(NodeLink(node.id, description))
        node.next.add(NodeLink(self.id, description))

    def update_playcount(self):
        self.playcount += 1