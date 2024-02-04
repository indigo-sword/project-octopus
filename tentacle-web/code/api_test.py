import requests
from uuid import uuid4
import random
import string

url = f'http://localhost:7809/'

import unittest

def random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

class TestApi(unittest.TestCase):
    def test_create_user(self):
        with self.subTest(msg="create user"):
            response = requests.post(url + "create_user", data={
                "username": str(uuid4()),
                "password": "password_4_joao",
                "email": random_email(),
            })

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["message"], "User created")
            self.assertTrue("user_id" in response.json())

        with self.subTest(msg="email already exists"):
            r = random_email()
            response = requests.post(url + "create_user", data={
                "username": str(uuid4()),
                "password": "password_4_joao",
                "email": r
            })

            self.assertEqual(response.status_code, 201)

            response = requests.post(url + "create_user", data={
                "username": str(uuid4()),
                "password": "password_4_joao",
                "email": r
            })

            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["message"], "Email already exists")

        with self.subTest(msg="username already exists"):
            r = str(uuid4())
            response = requests.post(url + "create_user", data={
                "username": r,
                "password": "password_4_joao",
                "email": random_email()
            })

            self.assertEqual(response.status_code, 201)

            response = requests.post(url + "create_user", data={
                "username": r,
                "password": "password_4_joao",
                "email": random_email()
            })

            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["message"], "Username already exists")


    def test_change_user_bio(self):
        with self.subTest("change user bio"):
            u = str(uuid4())
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "change_user_bio", data={
                "username": u,
                "bio": "I am Joao"
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "User bio updated")
            self.assertEqual(response.json()["bio"], "I am Joao")

        with self.subTest("user not found"):
            response = requests.post(url + "change_user_bio", data={
                "username": str(uuid4()),
                "bio": "I am Joao"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

def main():
    unittest.main()

if __name__ == "__main__":
    main()