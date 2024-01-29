from node import Node, NodeLink
from level import Level
from user import User
from db_manager import db_session
from sqlalchemy import or_

def save_test_node():
    testNode = Node(Level(0), User("joao", "idk", "jpireshe@nd.edu"), "test")
    testNode.save(db_session)
    print("saved!", testNode)

    return testNode.id

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

def test_link_nodes(id1: str, id2: str):
    testNodeOne = db_session.query(Node).filter(Node.id == f"{id1}").first()
    testNodeTwo = db_session.query(Node).filter(Node.id == f"{id2}").first()

    print("====== TEST NODES ======")
    print(testNodeOne, "\n", testNodeTwo)

    testNodeOne.link(testNodeTwo, "some description", db_session)

    result = db_session.query(NodeLink).filter(
            or_(
                (NodeLink.destination_id == "6ae19566-4c03-4222-84e2-c84d0d2bb118" and NodeLink.origin_id == "66b1afb7-2a31-48ed-876a-76457335914d"),
                (NodeLink.destination_id == "66b1afb7-2a31-48ed-876a-76457335914d" and NodeLink.origin_id == "6ae19566-4c03-4222-84e2-c84d0d2bb118")
            )
        ).all()
        
    print("====== RESULT ======")
    print(result)

def main():
    id1 = save_test_node()
    id2 = save_test_node()
    query_test_node(id1)
    edit_test_node_playcount(id1)
    edit_test_node_rating(id1, 4)

    # will always work
    test_link_nodes(id1, id2)

    # will never work
    test_link_nodes(id1, id2)

if __name__ == "__main__":
    main()