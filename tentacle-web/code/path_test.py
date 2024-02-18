from path import Path
from db_manager import db_session
from node import Node
from user import User
import unittest
from uuid import uuid4
import random
import string
from werkzeug.datastructures.file_storage import FileStorage


def random_email():
    return (
        "".join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"
    )


u = User(db_session, str(uuid4()), "PASS", random_email(), "BIO")


class TestPath(unittest.TestCase):
    def test_create_path(self):
        with self.subTest("create path"):
            p = Path(db_session, u, "TITLE", "DESCRIPTION")
            self.assertEqual(p.user_id, u.username)

            p2 = db_session.query(Path).filter(Path.id == p.id).first()
            self.assertEqual(p2.id, p.id)

    def test_add_node(self):
        # create a node
        with open("files/test.txt", "wb") as f:
            f.write(b"new file")
            f.seek(0)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename="test.txt")
            n1 = Node(db_session, u, "TITLE", "DESC", storage)

        with open("files/test.txt", "rb") as f:
            storage = FileStorage(f, filename="test.txt")
            n2 = Node(db_session, u, "TITLE", "DESC", storage)

        with self.subTest("add node in position zero"):
            p = Path(db_session, u, "TITLE", "DESCRIPTION")
            p.add_node(n1, 0, db_session)

            seq = p.get_node_sequence(db_session)
            self.assertEqual(len(seq), 1)
            self.assertEqual(seq[0].node_id, n1.id)
            self.assertEqual(seq[0].position, 0)
            self.assertEqual(p.position, 0)

        with self.subTest("add node in position one"):
            p.add_node(n2, 1, db_session)

            seq = p.get_node_sequence(db_session)
            self.assertEqual(len(seq), 2)
            self.assertEqual(seq[0].node_id, n1.id)
            self.assertEqual(seq[0].position, 0)
            self.assertEqual(seq[1].node_id, n2.id)
            self.assertEqual(seq[1].position, 1)
            self.assertEqual(p.position, 1)

        with self.subTest("add node in position zero when there is a zero already"):
            with open("files/test.txt", "rb") as f:
                storage = FileStorage(f, filename="test.txt")
                n3 = Node(db_session, u, "TITLE", "DESC", storage)

                try:  # add node in position zero
                    p.add_node(n3, 0, db_session)
                except Exception as e:
                    self.assertEqual(
                        str(e),
                        "invalid position - path already has node in position zero",
                    )

        with self.subTest("add node in position -1"):
            try:  # add node in position -1
                p.add_node(n3, -1, db_session)
            except Exception as e:
                self.assertEqual(str(e), "invalid position - negative")

        with self.subTest("add node in position 2"):
            p.add_node(n3, 2, db_session)

            seq = p.get_node_sequence(db_session)
            self.assertEqual(len(seq), 3)
            self.assertEqual(seq[0].node_id, n1.id)
            self.assertEqual(seq[0].position, 0)
            self.assertEqual(seq[1].node_id, n2.id)
            self.assertEqual(seq[1].position, 1)
            self.assertEqual(seq[2].node_id, n3.id)
            self.assertEqual(seq[2].position, 2)
            self.assertEqual(p.position, 2)

        with self.subTest("add another node in position 2"):
            with open("files/test.txt", "rb") as f:
                storage = FileStorage(f, filename="test.txt")
                n4 = Node(db_session, u, "TITLE", "DESC", storage)

            p.add_node(n4, 2, db_session)

            seq = p.get_node_sequence(db_session)
            self.assertEqual(len(seq), 4)
            self.assertEqual(seq[3].node_id, n4.id)
            self.assertEqual(seq[3].position, 2)
            self.assertEqual(p.position, 2)

        with self.subTest("add node in position 4"):
            with open("files/test.txt", "rb") as f:
                storage = FileStorage(f, filename="test.txt")
                n5 = Node(db_session, u, "TITLE", "DESC", storage)

            try:
                p.add_node(n5, 4, db_session)
            except Exception as e:
                self.assertEqual(str(e), "invalid position - no way to link")
                self.assertEqual(p.position, 2)

        with self.subTest("add node already in path"):
            try:
                p.add_node(n1, 3, db_session)
            except Exception as e:
                self.assertEqual(str(e), "node already in path")
                self.assertEqual(p.position, 2)

    def test_update_playcount(self):
        p = Path(db_session, u, "TAKEO'S ADVENTURE", "TAKEO IS A NICE GUY")
        p.update_playcount(db_session)

        self.assertEqual(p.playcount, 1)

        playcount = db_session.query(Path).filter(Path.id == p.id).first().playcount
        self.assertEqual(playcount, 1)

        p.update_playcount(db_session)

        self.assertEqual(p.playcount, 2)

        playcount = db_session.query(Path).filter(Path.id == p.id).first().playcount
        self.assertEqual(playcount, 2)

    def test_update_rating(self):
        p = Path(db_session, u, "TITLE", "DESCRIPTION")
        p.update_rating(5, db_session)

        self.assertEqual(p.rating, 5)

        rating = db_session.query(Path).filter(Path.id == p.id).first().rating
        self.assertEqual(rating, 5)

        p.update_rating(10, db_session)
        self.assertEqual(p.rating, 7.5)

        rating = db_session.query(Path).filter(Path.id == p.id).first().rating
        self.assertEqual(rating, 7.5)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
