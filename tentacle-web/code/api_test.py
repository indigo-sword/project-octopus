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
        response = requests.post(url + "create_user", data={
            "username": str(uuid4()),
            "password": "password_4_joao",
            "email": random_email(),
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User created")
        self.assertTrue("user_id" in response.json())

    def test_create_user_error_email(self):
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

    def test_create_user_error_username(self):
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

def main():
    e = random_email()
    u = str(uuid4())
    response = requests.post(url + "create_user", data={
        "username": u,
        "password": "password_4_joao",
        "email": e
    })
    uid = response.json()["user_id"]
    
    response = requests.post(url + "change_user_bio", data={
        "user_id": uid,
        "bio": "I am Joao"
    })

    response = requests.post(url + "change_user_bio", data={
        "username": u,
        "bio": "I am Joao2"
    })

    unittest.main()

if __name__ == "__main__":
    main()