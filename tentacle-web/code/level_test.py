from level import Level
from user import User
from db_manager import db_session
import unittest
import os

class TestLevel(unittest.TestCase):
    def test_create_level(self):
        u = User(db_session, "USERNAME", "PASS", "EMAIL", "SOME BIO")
        l = Level(db_session, u, b'TEST PASS')
        self.assertEqual(l.user_id, u.id)

        l = db_session.query(Level).filter(Level.id == l.id).first()
        self.assertEqual(l.user_id, u.id)

    def test_read_file(self):
        u = User(db_session, "USERNAME", "PASS", "EMAIL", "SOME BIO")
        l = Level(db_session, u, b'TEST PASS')

        self.assertEqual(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/levels/" + l.id + ".level", l.get_file_path())
        
        with open(l.get_file_path(), 'r') as f:
            self.assertEqual(f.read(), "TEST PASS")

            f.close()
    
def main():
    unittest.main()

if __name__ == "__main__":
    main()