from user import User, Follow, Friendship
from db_manager import db_session
from uuid import uuid4
import random
import string

def random_email():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"

def random_username():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

import unittest

class TestUser(unittest.TestCase):
    def test_create_user(self):
        i = random_username()
        e = random_email()
        u = User(db_session, i, "PASS", e, "SOME BIO")
        self.assertEqual(u.username, i)
        self.assertEqual(u.password, "PASS")
        self.assertEqual(u.email, e)
        self.assertEqual(u.bio, "SOME BIO")

    def test_update_bio(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u.update_bio(db_session, "NEW BIO")
        self.assertEqual(u.bio, "NEW BIO")

    def test_add_follower(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS2", random_email(), "SOME BIO2")
        u2.add_follower(db_session)
        self.assertEqual(u2.followers, 1)

        u2 = db_session.query(User).filter(User.username == u2.username).first()
        self.assertEqual(u2.followers, 1)

    def test_remove_follower(self):
        u2 = User(db_session, random_username(), "PASS2", random_email(), "SOME BIO2")
        u2.add_follower(db_session)
        u2.remove_follower(db_session)
        self.assertEqual(u2.followers, 0)

        u2 = db_session.query(User).filter(User.username == u2.username).first()
        self.assertEqual(u2.followers, 0)

    def test_add_following(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u.add_following(db_session)
        self.assertEqual(u.following, 1)

        u = db_session.query(User).filter(User.username == u.username).first()
        self.assertEqual(u.following, 1)

    def test_remove_following(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u.add_following(db_session)
        u.remove_following(db_session)
        self.assertEqual(u.following, 0)

        u = db_session.query(User).filter(User.username == u.username).first()
        self.assertEqual(u.following, 0)

    def test_follow(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")
        u.follow(db_session, u2)
        self.assertEqual(u.following, 1)
        self.assertEqual(u2.followers, 1)

        f = db_session.query(Follow).filter(Follow.follower == u.username).filter(Follow.followed == u2.username).first()
        self.assertIsNotNone(f)
        self.assertEqual(f.follower, u.username)
        self.assertEqual(f.followed, u2.username)
        

    def test_unfollow(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.follow(db_session, u2)
        u.unfollow(db_session, u2)

        self.assertEqual(u.following, 0)
        self.assertEqual(u2.followers, 0)

        f = db_session.query(Follow).filter(Follow.follower == u.username).filter(Follow.followed == u2.username).first()
        self.assertIsNone(f)

    def test_get_friends(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(db_session, u2)
        u2.accept_friend_request(db_session, u)

        f = u.get_friends(db_session)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].friend_one, u.username)
        self.assertEqual(f[0].friend_two, u2.username)

    def test_get_friend_requests(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(db_session, u2)

        f = u2.get_friend_requests(db_session)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].friend_one, u.username)
        self.assertEqual(f[0].friend_two, u2.username)

    def test_get_friend_requests_sent(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(db_session, u2)

        f = u.get_friend_requests_sent(db_session)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].friend_one, u.username)
        self.assertEqual(f[0].friend_two, u2.username)

    def test_accept_friend_request(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(db_session, u2)
        u2.accept_friend_request(db_session, u)

        f = db_session.query(Friendship).filter(Friendship.friend_one == u.username).filter(Friendship.friend_two == u2.username).first()
        self.assertEqual(f.status, 1)

    def test_send_friend_request(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(db_session, u2)

        f = db_session.query(Friendship).filter(Friendship.friend_one == u.username).filter(Friendship.friend_two == u2.username).first()
        self.assertEqual(f.status, 0)

    def test_remove_friend(self):
        u = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(db_session, u2)
        u2.accept_friend_request(db_session, u)

        u.remove_friend(db_session, u2)

        f = db_session.query(Friendship).filter(Friendship.friend_one == u.username).filter(Friendship.friend_two == u2.username).first()
        self.assertIsNone(f)

class TestFriendship(unittest.TestCase):
    def test_create_friendship(self):
        u1 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Friendship(db_session, u1, u2)
        self.assertEqual(f.friend_one, u1.username)
        self.assertEqual(f.friend_two, u2.username)
        f = db_session.query(Friendship).filter(Friendship.friend_one == u1.username).filter(Friendship.friend_two == u2.username).first()
        self.assertIsNotNone(f)

    def test_accept(self):
        u1 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Friendship(db_session, u1, u2)
        f.accept(db_session)
        self.assertEqual(f.status, 1)

        f = db_session.query(Friendship).filter(Friendship.friend_one == u1.username).filter(Friendship.friend_two == u2.username).first()
        self.assertEqual(f.status, 1)

    def test_reject(self):
        u1 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Friendship(db_session, u1, u2)
        f.reject(db_session)
        
        f = db_session.query(Friendship).filter(Friendship.friend_one == u1.username).filter(Friendship.friend_two == u2.username).first()
        self.assertIsNone(f)

    def test_get_followers(self):
        u1 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        u2.follow(db_session, u1)

        self.assertEqual(u1.get_followers(db_session), [u2.username])
        self.assertEqual(u1.get_following(db_session), [])
        self.assertEqual(u2.get_followers(db_session), [])
        self.assertEqual(u2.get_following(db_session), [u1.username])

class TestFollow(unittest.TestCase):
    def test_create_follow(self):
        u1 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Follow(db_session, u1, u2)
        self.assertEqual(f.follower, u1.username)
        self.assertEqual(f.followed, u2.username)

        f = db_session.query(Follow).filter(Follow.follower == u1.username).filter(Follow.followed == u2.username).first()
        self.assertIsNotNone(f)

    def test_unfollow(self):
        u1 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(db_session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Follow(db_session, u1, u2)
        f.unfollow(db_session)

        f = db_session.query(Follow).filter(Follow.follower == u1.username).filter(Follow.followed == u2.username).first()
        self.assertIsNone(f)

def main():
    unittest.main()

if __name__ == "__main__":
    main()