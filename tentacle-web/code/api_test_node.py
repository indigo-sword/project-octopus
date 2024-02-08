import requests
import random
import string
import werkzeug.datastructures

url = f'http://localhost:7809/'

import unittest
import os

def random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

def random_username():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

class TestApiNode(unittest.TestCase):
    def test_create_node(self):
        with self.subTest(msg="create node"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            with open("test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
            
            with open("test.txt", "rb") as f:
                response = requests.post(url + "create_node", data={
                    "username": u,
                    "description": "some description",
                }, files={"file": f})
                
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json()["message"], "Node created")
                self.assertTrue("node_id" in response.json())
                i = response.json()["node_id"]

            os.remove("test.txt")

            with open("../levels/" + i + ".level", "rb") as f:
                self.assertEqual(f.read(), b"THIS TEST HAS PASSED! 11")

        with self.subTest(msg="create node no username"):
            with open("test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()

            f = open("test.txt", "rb")

            response = requests.post(url + "create_node", data={
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="create node no description"):
            with open("test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()

            f = open("test.txt", "rb")

            response = requests.post(url + "create_node", data={
                "username": u,
            }, files={"file": f})

            f.close()

            os.remove("test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest(msg="create node no file"):
            response = requests.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            })
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no file parameter")

        with self.subTest(msg="create node no file data"):
            with open("test.txt", "wb") as f:
                f.close()

            f = open("test.txt", "rb")

            response = requests.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no file data")

        with self.subTest(msg="user does not exist"):
            with open("test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()
            
            f = open("test.txt", "rb")

            response = requests.post(url + "create_node", data={
                "username": "nonexistentuser",
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")



def main():
    unittest.main()

if __name__ == "__main__":
    main()

