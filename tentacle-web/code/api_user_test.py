import requests
import random
import string

url = f"http://64.225.11.30:8080/"

import unittest
import os


def random_email():
    return (
        "".join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"
    )


def random_username():
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


class TestApiUser(unittest.TestCase):
    def test_create_user(self):
        with self.subTest(msg="create user"):
            session = requests.Session()

            response = session.post(
                url + "create_user",
                data={
                    "username": random_username(),
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["message"], "user created")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()

            response = session.post(
                url + "create_user",
                data={
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no password parameter"):
            session = requests.Session()

            response = session.post(
                url + "create_user",
                data={
                    "username": random_username(),
                    "email": random_email(),
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no password parameter")

        with self.subTest(msg="no email parameter"):
            session = requests.Session()

            response = session.post(
                url + "create_user",
                data={
                    "username": random_username(),
                    "password": "password_4_joao",
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no email parameter")

        with self.subTest(msg="invalid email"):
            session = requests.Session()

            response = session.post(
                url + "create_user",
                data={
                    "username": random_username(),
                    "password": "password_4_joao",
                    "email": random_username(),
                },
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "invalid email")

        with self.subTest(msg="email already exists"):
            session = requests.Session()

            r = random_email()
            response = session.post(
                url + "create_user",
                data={
                    "username": random_username(),
                    "password": "password_4_joao",
                    "email": r,
                },
            )

            self.assertEqual(response.status_code, 201)

            response = session.post(
                url + "create_user",
                data={
                    "username": random_username(),
                    "password": "password_4_joao",
                    "email": r,
                },
            )

            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["message"], "email already exists")

        with self.subTest(msg="username already exists"):
            session = requests.Session()

            r = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": r,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            self.assertEqual(response.status_code, 201)

            response = session.post(
                url + "create_user",
                data={
                    "username": r,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["message"], "username already exists")

    def test_change_user_bio(self):
        with self.subTest("change user bio"):
            session = requests.Session()
            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "change_user_bio", data={"username": u, "bio": "I am Joao"}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "user bio updated")
            self.assertEqual(response.json()["bio"], "I am Joao")

        with self.subTest("no username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "change_user_bio", data={"bio": "I am Joao"})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no bio parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "change_user_bio", data={"username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no bio parameter")

        with self.subTest("user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "change_user_bio",
                data={"username": random_username(), "bio": "I am Joao"},
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "change_user_bio",
                data={"username": random_username(), "bio": "I am Joao"},
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

    def test_follow_user(self):
        with self.subTest("follow user"):
            session = requests.Session()

            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            response = session.post(
                url + "follow_user", data={"username": u, "followed_username": f}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "user followed")

        with self.subTest("no username parameter"):
            session = requests.Session()

            response = session.post(
                url + "follow_user", data={"followed_username": random_username()}
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no followed_username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "follow_user", data={"username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json()["message"], "no followed_username parameter"
            )

        with self.subTest("user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "follow_user",
                data={
                    "username": random_username(),
                    "followed_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "follow_user",
                data={
                    "username": random_username(),
                    "followed_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest("followed user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "follow_user",
                data={"username": u, "followed_username": random_username()},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "followed user not found")

    def test_unfollow_user(self):
        with self.subTest("unfollow user"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "follow_user", data={"username": u, "followed_username": f}
            )

            response = session.post(
                url + "unfollow_user", data={"username": u, "unfollowed_username": f}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "user unfollowed")

        with self.subTest("no username parameter"):
            response = session.post(
                url + "unfollow_user", data={"unfollowed_username": random_username()}
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no unfollowed_username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "unfollow_user", data={"username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json()["message"], "no unfollowed_username parameter"
            )

        with self.subTest("user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "unfollow_user",
                data={
                    "username": random_username(),
                    "unfollowed_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "unfollow_user",
                data={
                    "username": random_username(),
                    "unfollowed_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest("unfollowed user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "unfollow_user",
                data={"username": u, "unfollowed_username": random_username()},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "unfollowed user not found")

        with self.subTest("user is not being followed"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            response = session.post(
                url + "unfollow_user", data={"username": u, "unfollowed_username": f}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "user is not being followed")

    def test_get_follows(self):
        with self.subTest(msg="follow user"):
            sessionU = requests.Session()
            sessionF = requests.Session()
            sessionG = requests.Session()

            u = random_username()
            response = sessionU.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionU.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionF.post(
                url + "/login", data={"username": f, "password": "password_4_joao"}
            )

            g = random_username()
            sessionG.post(
                url + "create_user",
                data={
                    "username": g,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionG.post(
                url + "/login", data={"username": g, "password": "password_4_joao"}
            )

            sessionU.post(
                url + "follow_user", data={"username": u, "followed_username": f}
            )

            sessionF.post(
                url + "follow_user", data={"username": f, "followed_username": u}
            )

            sessionU.post(
                url + "follow_user", data={"username": u, "followed_username": g}
            )

            response = sessionU.get(url + "get_follows", data={"username": u})

            self.assertTrue(f in response.json()["following"])
            self.assertTrue(g in response.json()["following"])
            self.assertTrue(f in response.json()["followed"])
            self.assertFalse(g in response.json()["followed"])

        with self.subTest(msg="user not found"):
            session = requests.Session()

            u = random_username()

            response = session.get(url + "get_follows", data={"username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "user not found")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()

            response = session.get(url + "get_follows")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

    def test_add_friend(self):
        with self.subTest(msg="add friend"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            response = session.post(
                url + "add_friend", data={"username": u, "friend_username": f}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "friend request sent")

        with self.subTest(msg="already friends"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionF.post(
                url + "/login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(
                url + "add_friend", data={"username": u, "friend_username": f}
            )

            self.assertEqual(response.json()["message"], "user is already a friend")

        with self.subTest(msg="friend request already sent"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = session.post(
                url + "add_friend", data={"username": u, "friend_username": f}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "friend request already sent")

        with self.subTest(msg="friend request already received from other user"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            sessionF.post(
                url + "add_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(
                url + "add_friend", data={"username": u, "friend_username": f}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "friend request accepted")

        with self.subTest(msg="no username parameter"):
            response = session.post(
                url + "add_friend", data={"friend_username": random_username()}
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "add_friend", data={"username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "add_friend",
                data={
                    "username": random_username(),
                    "friend_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest(msg="user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "add_friend",
                data={
                    "username": random_username(),
                    "friend_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest(msg="friend user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "add_friend",
                data={"username": u, "friend_username": random_username()},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "friend user not found")

    def test_accept_friend(self):
        with self.subTest(msg="accept friend"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "friend request accepted")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(url + "accept_friend", data={"friend_username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend",
                data={
                    "username": f,
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "accept_friend",
                data={
                    "username": random_username(),
                    "friend_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest(msg="user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend",
                data={"username": random_username(), "friend_username": u},
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest(msg="friend user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend",
                data={"username": f, "friend_username": random_username()},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "friend user not found")

        with self.subTest(msg="no friend request from this user"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["message"], "no friend request from this user"
            )

    def test_reject_friend(self):
        with self.subTest(msg="reject friend"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "reject_friend", data={"username": f, "friend_username": u}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "friend request rejected")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(url + "reject_friend", data={"friend_username": u})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(url + "reject_friend", data={"username": f})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "reject_friend",
                data={
                    "username": random_username(),
                    "friend_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest(msg="user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "reject_friend",
                data={"username": random_username(), "friend_username": u},
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest(msg="friend user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "reject_friend",
                data={"username": f, "friend_username": random_username()},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "friend user not found")

        with self.subTest(msg="no friend request from this user"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            response = sessionF.post(
                url + "reject_friend", data={"username": f, "friend_username": u}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["message"], "no friend request from this user"
            )

    def test_remove_friend(self):
        with self.subTest(msg="remove friend"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(
                url + "remove_friend", data={"username": u, "friend_username": f}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "friend removed")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(url + "remove_friend", data={"friend_username": f})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(
                url + "remove_friend",
                data={
                    "username": u,
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not logged in"):
            session = requests.Session()

            response = session.post(
                url + "remove_friend",
                data={
                    "username": random_username(),
                    "friend_username": random_username(),
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest(msg="user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(
                url + "remove_friend",
                data={"username": random_username(), "friend_username": f},
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest(msg="friend user not found"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            session.post(url + "add_friend", data={"username": u, "friend_username": f})

            response = sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            response = session.post(
                url + "remove_friend",
                data={"username": u, "friend_username": random_username()},
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "friend user not found")

        with self.subTest(msg="user is not a friend"):
            session = requests.Session()

            u = random_username()
            response = session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            f = random_username()
            sessionF = requests.Session()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )
            sessionF.post(
                url + "login", data={"username": f, "password": "password_4_joao"}
            )

            response = session.post(
                url + "remove_friend", data={"username": u, "friend_username": f}
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "user is not a friend")

    def test_get_friends(self):
        with self.subTest(msg="get friends"):
            sessionU = requests.Session()
            u = random_username()
            sessionU.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionU.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            sessionF = requests.Session()
            f = random_username()
            sessionF.post(
                url + "create_user",
                data={
                    "username": f,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionF.post(
                url + "/login", data={"username": f, "password": "password_4_joao"}
            )

            sessionG = requests.Session()
            g = random_username()
            sessionG.post(
                url + "create_user",
                data={
                    "username": g,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionG.post(
                url + "/login", data={"username": g, "password": "password_4_joao"}
            )

            sessionH = requests.Session()
            h = random_username()
            sessionH.post(
                url + "create_user",
                data={
                    "username": h,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionH.post(
                url + "/login", data={"username": h, "password": "password_4_joao"}
            )

            sessionI = requests.Session()
            i = random_username()
            sessionI.post(
                url + "create_user",
                data={
                    "username": i,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionI.post(
                url + "/login", data={"username": i, "password": "password_4_joao"}
            )

            sessionJ = requests.Session()
            j = random_username()
            sessionJ.post(
                url + "create_user",
                data={
                    "username": j,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            sessionJ.post(
                url + "/login", data={"username": j, "password": "password_4_joao"}
            )

            sessionU.post(
                url + "add_friend", data={"username": u, "friend_username": f}
            )

            # f accepts
            sessionF.post(
                url + "accept_friend", data={"username": f, "friend_username": u}
            )

            # g will be left pending
            sessionU.post(
                url + "add_friend", data={"username": u, "friend_username": g}
            )

            # h added u
            sessionH.post(
                url + "add_friend", data={"username": h, "friend_username": u}
            )

            # i adds u but u refuses
            sessionI.post(
                url + "add_friend", data={"username": i, "friend_username": u}
            )

            sessionU.post(
                url + "reject_friend", data={"username": u, "friend_username": i}
            )

            # u adds j but j refuses
            sessionU.post(
                url + "add_friend", data={"username": u, "friend_username": j}
            )

            sessionJ.post(
                url + "reject_friend", data={"username": j, "friend_username": u}
            )

            response = sessionU.get(url + "get_friends", data={"username": u})

            self.assertTrue(f in response.json()["friends"])
            self.assertFalse(
                any([x in response.json()["friends"] for x in [g, h, i, j]])
            )

            self.assertTrue(h in response.json()["requests"])
            self.assertFalse(
                any([x in response.json()["requests"] for x in [f, g, i, j]])
            )

            self.assertTrue(g in response.json()["sent requests"])
            self.assertFalse(
                any([x in response.json()["sent requests"] for x in [f, h, i, j]])
            )

        with self.subTest(msg="user not found"):
            session = requests.Session()

            response = session.get(
                url + "get_friends", data={"username": random_username()}
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "user not found")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()

            response = session.get(url + "get_friends")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

    def test_get_user(self):
        with self.subTest(msg="get user"):
            session = requests.Session()
            u = random_username()
            e = random_email()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": e,
                    "bio": "I am Joao",
                },
            )

            response = session.get(url + "get_user", data={"username": u})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["username"], u)
            self.assertEqual(response.json()["email"], e)
            self.assertEqual(response.json()["bio"], "I am Joao")
            self.assertEqual(response.json()["following"], 0)
            self.assertEqual(response.json()["followers"], 0)

        with self.subTest(msg="user not found"):
            session = requests.Session()
            response = session.get(
                url + "get_user", data={"username": "this username does not exist"}
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "user not found")

        with self.subTest(msg="no username parameter"):
            session = requests.Session()
            response = session.get(url + "get_user")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

    def test_login(self):
        with self.subTest("login"):
            session = requests.Session()

            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            response = session.post(
                url + "login", data={"username": u, "password": "password_4_joao"}
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "user logged in")

        with self.subTest("wrong password"):
            session = requests.Session()

            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            response = session.post(
                url + "login", data={"username": u, "password": "wrong_password"}
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "invalid password")

        with self.subTest("user not found"):
            session = requests.Session()
            response = session.post(
                url + "login",
                data={
                    "username": "this username does not exist",
                    "password": "password",
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "user not found")

        with self.subTest("no username parameter"):
            session = requests.Session()
            response = session.post(url + "login", data={"password": "password"})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no password parameter"):
            session = requests.Session()
            response = session.post(url + "login", data={"username": "username"})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no password parameter")

    def test_logout(self):
        with self.subTest("logged out"):
            session = requests.Session()
            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "/logout", data={"username": u})

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "logged out")

        with self.subTest("user not logged in"):
            session = requests.Session()
            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            response = session.post(url + "/logout", data={"username": u})

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("no username parameter"):
            session = requests.Session()
            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(url + "/logout", data={})

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("wrong user for logout"):
            session = requests.Session()
            u = random_username()
            session.post(
                url + "create_user",
                data={
                    "username": u,
                    "password": "password_4_joao",
                    "email": random_email(),
                },
            )

            session.post(
                url + "/login", data={"username": u, "password": "password_4_joao"}
            )

            response = session.post(
                url + "/logout", data={"username": random_username()}
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")


def main():
    unittest.main(warnings="ignore")


if __name__ == "__main__":
    main()
