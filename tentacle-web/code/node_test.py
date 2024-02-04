from node import Node, NodeLink
from level import Level
from user import User
from db_manager import db_session
from sqlalchemy import or_
import unittest

class TestNode(unittest.TestCase):
    def test_save_node(self):
        u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")
        testNode = Node(db_session, Level(db_session, u, b''), u, "DESC")
        self.assertIsNotNone(testNode.id)

        t = db_session.query(Node).filter(Node.id == testNode.id).first()
        self.assertIsNotNone(t)

    def test_link(self):
        u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")
        testNodeOne = Node(db_session, Level(db_session, u, b''), u, "DESC")
        testNodeTwo = Node(db_session, Level(db_session, u, b''), u, "DESC")

        testNodeOne.link(testNodeTwo, "some description", db_session)

        result = db_session.query(NodeLink).filter(
            or_(
                (NodeLink.destination_id == testNodeOne.id and NodeLink.origin_id == testNodeTwo.id),
                (NodeLink.destination_id == testNodeTwo.id and NodeLink.origin_id == testNodeOne.id)
            )
        ).all()
        
        self.assertIsNotNone(result)

    def test_link_fail(self):
        u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")
        testNodeOne = Node(db_session, Level(db_session, u, b''), u, "DESC")
        testNodeTwo = Node(db_session, Level(db_session, u, b''), u, "DESC")

        testNodeOne.link(testNodeTwo, "some description", db_session)

        with self.assertRaises(Exception):
            testNodeOne.link(testNodeTwo, "some description", db_session)

    def test_update_playcount(self):
        u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")
        testNode = Node(db_session, Level(db_session, u, b''), u, "DESC")
        testNode.update_playcount(db_session)
        self.assertEqual(testNode.get_playcount(), 1)

        playcount = db_session.query(Node).filter(Node.id == testNode.id).first().playcount
        self.assertEqual(playcount, 1)

    def test_update_rating(self):
        u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")
        testNode = Node(db_session, Level(db_session, u, b''), u, "DESC")
        testNode.update_rating(5, db_session)
        self.assertEqual(testNode.get_rating(), 5)

        rating = db_session.query(Node).filter(Node.id == testNode.id).first().rating
        self.assertEqual(rating, 5)

def main():
    unittest.main()

if __name__ == "__main__":
    main()