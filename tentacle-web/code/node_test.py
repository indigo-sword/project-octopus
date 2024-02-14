from node import Node, NodeLink
from user import User
from db_manager import db_session
from sqlalchemy import or_, and_
import unittest
import os
from uuid import uuid4
import random
import string
from werkzeug.datastructures.file_storage import FileStorage
import tempfile

def random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

class TestNode(unittest.TestCase):
    def test_save_node(self):
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')

            u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
            testNode = Node(db_session, u, "DESC", storage)
            self.assertIsNotNone(testNode.id)

            t = db_session.query(Node).filter(Node.id == testNode.id).first()
            self.assertIsNotNone(t)

        os.remove("files/test.txt")

    def test_link(self):
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
            testNodeOne = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
            testNodeTwo = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

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
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNodeOne = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNodeTwo = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        testNodeOne.link(testNodeTwo, "some description", db_session)

        with self.assertRaises(Exception):
            testNodeOne.link(testNodeTwo, "some description", db_session)

    def test_link_fail_is_initial(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNodeOne = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNodeTwo = Node(db_session, u, "DESC", storage, is_initial=True)

        os.remove("files/test.txt")

        try: testNodeOne.link(testNodeTwo, "some description", db_session)
        except Exception as e: self.assertEqual(str(e), "cannot link to initial node")

    def test_link_fail_self(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNodeOne = Node(db_session, u, "DESC", storage, is_final=True)

        os.remove("files/test.txt")

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNodeTwo = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        try: testNodeOne.link(testNodeTwo, "some description", db_session)
        except Exception as e: self.assertEqual(str(e), "cannot link from final node")

    def test_update_playcount(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNode = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        testNode.update_playcount(db_session)
        self.assertEqual(testNode.get_playcount(), 1)

        playcount = db_session.query(Node).filter(Node.id == testNode.id).first().playcount
        self.assertEqual(playcount, 1)

    def test_update_rating(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            testNode = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        testNode.update_rating(5, db_session)
        self.assertEqual(testNode.get_rating(), 5)

        rating = db_session.query(Node).filter(Node.id == testNode.id).first().rating
        self.assertEqual(rating, 5)

    def test_read_file(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        self.assertEqual(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/levels/" + n.id + ".level", n.get_file_path())
        
        with open(n.get_file_path(), 'r') as f:
            self.assertEqual(f.read(), "THIS TEST HAS PASSED! 11")
            f.close()

    def test_get_next_links(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n1 = Node(db_session, u, "DESC", storage)
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n2 = Node(db_session, u, "DESC", storage)
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n3 = Node(db_session, u, "DESC", storage)
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n4 = Node(db_session, u, "DESC", storage)
            f.seek(0)

        n1.link(n2, "some description", db_session)
        n1.link(n3, "some description", db_session)

        self.assertTrue(n2.id in [n.destination_id for n in n1.get_next_links(db_session)])
        self.assertTrue(n3.id in [n.destination_id for n in n1.get_next_links(db_session)])
        self.assertFalse(n4.id in [n.destination_id for n in n1.get_next_links(db_session)])

        os.remove("files/test.txt")

    def test_get_previous_links(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n1 = Node(db_session, u, "DESC1", storage)
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n2 = Node(db_session, u, "DESC2", storage)
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n3 = Node(db_session, u, "DESC3", storage)
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n4 = Node(db_session, u, "DESC4", storage)
            f.seek(0)
        
        n1.link(n2, "some description1", db_session)
        n2.link(n3, "some description2", db_session)
        n3.link(n4, "some description3", db_session)

        self.assertTrue(n1.id in [n.origin_id for n in n2.get_previous_links(db_session)])
        self.assertTrue(n2.id in [n.origin_id for n in n3.get_previous_links(db_session)])
        self.assertTrue(n3.id in [n.origin_id for n in n4.get_previous_links(db_session)])

class TestNodeLink(unittest.TestCase):
    def test_create_nodelink(self):
        u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")
        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n1 = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename='test.txt')
            n2 = Node(db_session, u, "DESC", storage)

        os.remove("files/test.txt")

        l = NodeLink(db_session, n1, n2, "DESC")
        self.assertEqual(l.origin_id, n1.id)
        self.assertEqual(l.destination_id, n2.id)

        l2 = db_session.query(NodeLink).filter(NodeLink.id == l.id).first()
        self.assertEqual(l2.id, l.id)

def main():
    unittest.main()

if __name__ == "__main__":
    main()