import requests
import random
import string

url = f'http://localhost:7809/'

import unittest

def random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

def random_username():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

class TestApiUser(unittest.TestCase):
    def test_create_user(self):
        with self.subTest(msg="create user"):
            response = requests.post(url + "create_user", data={
                "username": random_username(),
                "password": "password_4_joao",
                "email": random_email(),
            })

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["message"], "User created")

        with self.subTest(msg="no username parameter"):
            response = requests.post(url + "create_user", data={
                "password": "password_4_joao",
                "email": random_email(),
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no password parameter"):
            response = requests.post(url + "create_user", data={
                "username": random_username(),
                "email": random_email(),
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no password parameter")

        with self.subTest(msg="no email parameter"):
            response = requests.post(url + "create_user", data={
                "username": random_username(),
                "password": "password_4_joao",
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no email parameter")

        with self.subTest(msg="invalid email"):
            response = requests.post(url + "create_user", data={
                "username": random_username(),
                "password": "password_4_joao",
                "email": random_username(),
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "Invalid email")

        with self.subTest(msg="email already exists"):
            r = random_email()
            response = requests.post(url + "create_user", data={
                "username": random_username(),
                "password": "password_4_joao",
                "email": r
            })

            self.assertEqual(response.status_code, 201)

            response = requests.post(url + "create_user", data={
                "username": random_username(),
                "password": "password_4_joao",
                "email": r
            })

            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.json()["message"], "Email already exists")

        with self.subTest(msg="username already exists"):
            r = random_username()
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
            u = random_username()
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

        with self.subTest("no username parameter"):
            response = requests.post(url + "change_user_bio", data={
                "bio": "I am Joao"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no bio parameter"):
            response = requests.post(url + "change_user_bio", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no bio parameter")

        with self.subTest("user not found"):
            response = requests.post(url + "change_user_bio", data={
                "username": random_username(),
                "bio": "I am Joao"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

    def test_follow_user(self):
        with self.subTest("follow user"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "follow_user", data={
                "username": u,
                "followed_username": f
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "User followed")

        with self.subTest("no username parameter"):
            response = requests.post(url + "follow_user", data={
                "followed_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no followed_username parameter"):
            response = requests.post(url + "follow_user", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no followed_username parameter")

        with self.subTest("user not found"):
            response = requests.post(url + "follow_user", data={
                "username": random_username(),
                "followed_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest("followed user not found"):
            u = random_username()
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "follow_user", data={
                "username": u,
                "followed_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "Followed user not found")

    def test_unfollow_user(self):
        with self.subTest("unfollow user"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "follow_user", data={
                "username": u,
                "followed_username": f
            })

            response = requests.post(url + "unfollow_user", data={
                "username": u,
                "unfollowed_username": f
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "User unfollowed")

        with self.subTest("no username parameter"):
            response = requests.post(url + "unfollow_user", data={
                "unfollowed_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("no unfollowed_username parameter"):
            response = requests.post(url + "unfollow_user", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no unfollowed_username parameter")

        with self.subTest("user not found"):
            response = requests.post(url + "unfollow_user", data={
                "username": random_username(),
                "unfollowed_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest("unfollowed user not found"):
            u = random_username()
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "unfollow_user", data={
                "username": u,
                "unfollowed_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "Unfollowed user not found")

        with self.subTest("user is not being followed"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "unfollow_user", data={
                "username": u,
                "unfollowed_username": f
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "User is not being followed")

    def test_get_follows(self):
        with self.subTest(msg="follow user"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            g = random_username()
            requests.post(url + "create_user", data={
                "username": g,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "follow_user", data={
                "username": u,
                "followed_username": f
            })

            requests.post(url + "follow_user", data={
                "username": f,
                "followed_username": u
            })

            requests.post(url + "follow_user", data={
                "username": u,
                "followed_username": g
            })

            response = requests.get(url + "get_follows", data={
                "username": u
            })

            self.assertTrue(f in response.json()["following"])
            self.assertTrue(g in response.json()["following"])
            self.assertTrue(f in response.json()["followed"])
            self.assertFalse(g in response.json()["followed"])

        with self.subTest(msg="user not found"):
            u = random_username()
            response = requests.get(url + "get_follows", data={
                "username": u
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest(msg="no username parameter"):
            response = requests.get(url + "get_follows")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

    def test_add_friend(self):
        with self.subTest(msg="add friend"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Friend request sent")   

        with self.subTest(msg="already friends"):  
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            requests.post(url + "accept_friend", data={
                "username": f,
                "friend_username": u
            })

            response = requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.json()["message"], "User is already a friend")    
        
        with self.subTest(msg="friend request already sent"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            response = requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "Friend request already sent")
        
        with self.subTest(msg="friend request already received from other user"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": f,
                "friend_username": u
            })

            response = requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Friend request accepted")

        with self.subTest(msg="no username parameter"):
            response = requests.post(url + "add_friend", data={
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            response = requests.post(url + "add_friend", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not found"):
            response = requests.post(url + "add_friend", data={
                "username": random_username(),
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest(msg="friend user not found"):
            u = random_username()
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "Friend user not found")

    def test_accept_friend(self):
        with self.subTest(msg="accept friend"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            response = requests.post(url + "accept_friend", data={
                "username": f,
                "friend_username": u
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Friend request accepted")

        with self.subTest(msg="no username parameter"):
            response = requests.post(url + "accept_friend", data={
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            response = requests.post(url + "accept_friend", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not found"):
            response = requests.post(url + "accept_friend", data={
                "username": random_username(),
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest(msg="friend user not found"):
            u = random_username()
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "accept_friend", data={
                "username": u,
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "Friend user not found")

        with self.subTest(msg="no friend request from this user"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "accept_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "No friend request from this user")

    def test_reject_friend(self):
        with self.subTest(msg="reject friend"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            response = requests.post(url + "reject_friend", data={
                "username": f,
                "friend_username": u
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Friend request rejected")

        with self.subTest(msg="no username parameter"):
            response = requests.post(url + "reject_friend", data={
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="no friend_username parameter"):
            response = requests.post(url + "reject_friend", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")
        
        with self.subTest(msg="user not found"):
            response = requests.post(url + "reject_friend", data={
                "username": random_username(),
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest(msg="friend user not found"):
            u = random_username()
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "reject_friend", data={
                "username": u,
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "Friend user not found")
        
        with self.subTest(msg="no friend request from this user"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "reject_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "No friend request from this user")

    def test_remove_friend(self):
        with self.subTest(msg="remove friend"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            requests.post(url + "accept_friend", data={
                "username": f,
                "friend_username": u
            })

            response = requests.post(url + "remove_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "Friend removed")

        with self.subTest(msg="no username parameter"):
            response = requests.post(url + "remove_friend", data={
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")
        
        with self.subTest(msg="no friend_username parameter"):
            response = requests.post(url + "remove_friend", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no friend_username parameter")

        with self.subTest(msg="user not found"):
            response = requests.post(url + "remove_friend", data={
                "username": random_username(),
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")
        
        with self.subTest(msg="friend user not found"):
            u = random_username()
            response = requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "remove_friend", data={
                "username": u,
                "friend_username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "Friend user not found")
        
        with self.subTest(msg="user is not a friend"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = requests.post(url + "remove_friend", data={
                "username": u,
                "friend_username": f
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "User is not a friend")
    
    def test_get_friends(self):
        with self.subTest(msg="get friends"):
            u = random_username()
            requests.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            f = random_username()
            requests.post(url + "create_user", data={
                "username": f,
                "password": "password_4_joao",
                "email": random_email()
            })

            g = random_username()
            requests.post(url + "create_user", data={
                "username": g,
                "password": "password_4_joao",
                "email": random_email()
            })

            h = random_username()
            requests.post(url + "create_user", data={
                "username": h,
                "password": "password_4_joao",
                "email": random_email()
            })

            i = random_username()
            requests.post(url + "create_user", data={
                "username": i,
                "password": "password_4_joao",
                "email": random_email()
            })

            j = random_username()
            requests.post(url + "create_user", data={
                "username": j,
                "password": "password_4_joao",
                "email": random_email()
            })

            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": f
            })

            # f accepts
            requests.post(url + "accept_friend", data={
                "username": f,
                "friend_username": u
            })

            # g will be left pending
            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": g
            })

            # h added u
            requests.post(url + "add_friend", data={
                "username": h,
                "friend_username": u
            })

            # i adds u but u refuses
            requests.post(url + "add_friend", data={
                "username": i,
                "friend_username": u
            })

            requests.post(url + "reject_friend", data={
                "username": u,
                "friend_username": i
            })

            # u adds j but j refuses
            requests.post(url + "add_friend", data={
                "username": u,
                "friend_username": j
            })

            requests.post(url + "reject_friend", data={
                "username": j,
                "friend_username": u
            })

            response = requests.get(url + "get_friends", data={
                "username": u
            })

            self.assertTrue(f in response.json()["friends"])
            self.assertFalse(any([x in response.json()["friends"] for x in [g, h, i, j]]))

            self.assertTrue(h in response.json()["requests"])
            self.assertFalse(any([x in response.json()["requests"] for x in [f, g, i, j]]))

            self.assertTrue(g in response.json()["sent requests"])
            self.assertFalse(any([x in response.json()["sent requests"] for x in [f, h, i, j]]))

        with self.subTest(msg="user not found"):
            response = requests.get(url + "get_friends", data={
                "username": random_username()
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "User not found")

        with self.subTest(msg="no username parameter"):
            response = requests.get(url + "get_friends")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")


def main():
    unittest.main()

if __name__ == "__main__":
    main()