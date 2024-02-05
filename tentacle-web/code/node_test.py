from node import Node, NodeLink
from user import User
from db_manager import db_session
from sqlalchemy import or_
import unittest
import os
from uuid import uuid4
import random
import string

def random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

class TestNode(unittest.TestCase):
    def test_save_node(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        testNode = Node(db_session, u, "DESC", b'LEVEL')
        self.assertIsNotNone(testNode.id)

        t = db_session.query(Node).filter(Node.id == testNode.id).first()
        self.assertIsNotNone(t)

    def test_link(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        testNodeOne = Node(db_session, u, "DESC", b'LEVEL')
        testNodeTwo = Node(db_session, u, "DESC", b'LEVEL')

        testNodeOne.link(testNodeTwo, "some description", db_session)

        result = db_session.query(NodeLink).filter(
            or_(
                (NodeLink.destination_id == testNodeOne.id and NodeLink.origin_id == testNodeTwo.id),
                (NodeLink.destination_id == testNodeTwo.id and NodeLink.origin_id == testNodeOne.id)
            )
        ).all()
        
        self.assertIsNotNone(result)

    def test_link_fail(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        testNodeOne = Node(db_session, u, "DESC", b'LEVEL')
        testNodeTwo = Node(db_session, u, "DESC", b'LEVEL')

        testNodeOne.link(testNodeTwo, "some description", db_session)

        with self.assertRaises(Exception):
            testNodeOne.link(testNodeTwo, "some description", db_session)

    def test_update_playcount(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        testNode = Node(db_session, u, "DESC", b'LEVEL')
        testNode.update_playcount(db_session)
        self.assertEqual(testNode.get_playcount(), 1)

        playcount = db_session.query(Node).filter(Node.id == testNode.id).first().playcount
        self.assertEqual(playcount, 1)

    def test_update_rating(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        testNode = Node(db_session, u, "DESC", b'LEVEL')
        testNode.update_rating(5, db_session)
        self.assertEqual(testNode.get_rating(), 5)

        rating = db_session.query(Node).filter(Node.id == testNode.id).first().rating
        self.assertEqual(rating, 5)

    def test_read_file(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        
        n = Node(db_session, u, "DESC", b'TEST PASS')

        self.assertEqual(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/levels/" + n.id + ".level", n.get_file_path())
        
        with open(n.get_file_path(), 'r') as f:
            self.assertEqual(f.read(), "TEST PASS")
            f.close()

class TestNodeLink(unittest.TestCase):
    def test_create_nodelink(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        n1 = Node(db_session, u, "DESC", b'LEVEL')
        n2 = Node(db_session, u, "DESC", b'LEVEL')

        l = NodeLink(db_session, n1, n2, "DESC")
        self.assertEqual(l.origin_id, n1.id)
        self.assertEqual(l.destination_id, n2.id)

        l2 = db_session.query(NodeLink).filter(NodeLink.id == l.id).first()
        self.assertEqual(l2.id, l.id)

def main():
    unittest.main()

if __name__ == "__main__":
    main()