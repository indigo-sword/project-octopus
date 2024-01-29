from node import Node
from level import Level
from user import User
from db_manager import db_session

def save_test_node():
    # RUN ONLY ONCE (already done)
    testNode = Node(Level(1), User("joao", "idk", "jpireshe@nd.edu"), "test")
    testNode.save(db_session)
    print("saved!")
    # id: dce8edf2-cb14-47a3-92cc-b6e1e856b5ba

def query_test_node(id: str):
    testNode = db_session.query(Node).filter(Node.id == f"{id}").first()
    print(testNode)

def edit_test_node_playcount(id: str):
    testNode = db_session.query(Node).filter(Node.id == f"{id}").first()
    testNode.update_playcount(db_session)
    print(testNode)
    print(testNode.get_playcount())

def edit_test_node_rating(id: str):
    testNode = db_session.query(Node).filter(Node.id == f"{id}").first()
    testNode.update_rating(5, db_session)
    print(testNode)
    print(testNode.get_rating())

def main():
    testNodeId = 'dce8edf2-cb14-47a3-92cc-b6e1e856b5ba'
    query_test_node(testNodeId)
    edit_test_node_playcount(testNodeId)
    edit_test_node_rating(testNodeId)

if __name__ == "__main__":
    main()