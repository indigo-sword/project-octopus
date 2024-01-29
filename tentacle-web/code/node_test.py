from node import Node
from level import Level
from user import User
from db_manager import db_session

def save_test_node():
    # RUN ONLY ONCE (already done)
    testNode = Node(Level(1), User("joao", "idk", "jpireshe@nd.edu"), "test")
    testNode.save(db_session)
    print("saved!", testNode)
    # id: 6ae19566-4c03-4222-84e2-c84d0d2bb118

def query_test_node(id: str):
    testNode = db_session.query(Node).filter(Node.id == f"{id}").first()
    print("===== QUERIED =====", testNode)

def edit_test_node_playcount(id: str):
    testNode = db_session.query(Node).filter(Node.id == f"{id}").first()
    testNode.update_playcount(db_session)
    print("===== EDITED PLAYCOUNT =====", testNode)
    print(testNode.get_playcount())

def edit_test_node_rating(id: str, rating: int):
    testNode = db_session.query(Node).filter(Node.id == f"{id}").first()
    testNode.update_rating(4, db_session)
    print("===== EDITED RATING =====", testNode)
    print(testNode.get_rating())

def main():
    testNodeId = "6ae19566-4c03-4222-84e2-c84d0d2bb118"
    query_test_node(testNodeId)
    edit_test_node_playcount(testNodeId)
    edit_test_node_rating(testNodeId, 4)

if __name__ == "__main__":
    main()