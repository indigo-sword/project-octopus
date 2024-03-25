from user import User, Follow, Friendship
from db_manager import Session
from uuid import uuid4
import random
import string


def random_email():
    return (
        "".join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"
    )


def random_username():
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


import unittest


class TestUser(unittest.TestCase):
    def test_create_user(self):
        i = random_username()
        e = random_email()
        u = User(Session, i, "PASS", e, "SOME BIO")
        self.assertEqual(u.username, i)
        self.assertEqual(u.email, e)
        self.assertEqual(u.bio, "SOME BIO")

    def test_update_bio(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u.update_bio(Session, "NEW BIO")
        self.assertEqual(u.bio, "NEW BIO")

    def test_add_follower(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS2", random_email(), "SOME BIO2")
        u2.add_follower(Session)
        self.assertEqual(u2.followers, 1)

        u2 = Session.query(User).filter(User.username == u2.username).first()
        self.assertEqual(u2.followers, 1)

    def test_remove_follower(self):
        u2 = User(Session, random_username(), "PASS2", random_email(), "SOME BIO2")
        u2.add_follower(Session)
        u2.remove_follower(Session)
        self.assertEqual(u2.followers, 0)

        u2 = Session.query(User).filter(User.username == u2.username).first()
        self.assertEqual(u2.followers, 0)

    def test_add_following(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u.add_following(Session)
        self.assertEqual(u.following, 1)

        u = Session.query(User).filter(User.username == u.username).first()
        self.assertEqual(u.following, 1)

    def test_remove_following(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u.add_following(Session)
        u.remove_following(Session)
        self.assertEqual(u.following, 0)

        u = Session.query(User).filter(User.username == u.username).first()
        self.assertEqual(u.following, 0)

    def test_follow(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")
        u.follow(Session, u2)
        self.assertEqual(u.following, 1)
        self.assertEqual(u2.followers, 1)

        f = (
            Session.query(Follow)
            .filter(Follow.follower == u.username)
            .filter(Follow.followed == u2.username)
            .first()
        )
        self.assertIsNotNone(f)
        self.assertEqual(f.follower, u.username)
        self.assertEqual(f.followed, u2.username)

    def test_unfollow(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.follow(Session, u2)
        u.unfollow(Session, u2)

        self.assertEqual(u.following, 0)
        self.assertEqual(u2.followers, 0)

        f = (
            Session.query(Follow)
            .filter(Follow.follower == u.username)
            .filter(Follow.followed == u2.username)
            .first()
        )
        self.assertIsNone(f)

    def test_get_friends(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(Session, u2)
        u2.accept_friend_request(Session, u)

        f = u.get_friends(Session)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0], u2.username)

    def test_get_friend_requests(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(Session, u2)

        f = u2.get_friend_requests(Session)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0], u.username)

    def test_get_friend_requests_sent(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(Session, u2)

        f = u.get_friend_requests_sent(Session)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0], u2.username)

    def test_accept_friend_request(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(Session, u2)
        u2.accept_friend_request(Session, u)

        f = (
            Session.query(Friendship)
            .filter(Friendship.friend_one == u.username)
            .filter(Friendship.friend_two == u2.username)
            .first()
        )
        self.assertEqual(f.status, 1)

    def test_send_friend_request(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(Session, u2)

        f = (
            Session.query(Friendship)
            .filter(Friendship.friend_one == u.username)
            .filter(Friendship.friend_two == u2.username)
            .first()
        )
        self.assertEqual(f.status, 0)

    def test_remove_friend(self):
        u = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u.send_friend_request(Session, u2)
        u2.accept_friend_request(Session, u)

        u.remove_friend(Session, u2)

        f = (
            Session.query(Friendship)
            .filter(Friendship.friend_one == u.username)
            .filter(Friendship.friend_two == u2.username)
            .first()
        )
        self.assertIsNone(f)


class TestFriendship(unittest.TestCase):
    def test_create_friendship(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Friendship(Session, u1, u2)
        self.assertEqual(f.friend_one, u1.username)
        self.assertEqual(f.friend_two, u2.username)
        f = (
            Session.query(Friendship)
            .filter(Friendship.friend_one == u1.username)
            .filter(Friendship.friend_two == u2.username)
            .first()
        )
        self.assertIsNotNone(f)

    def test_accept(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Friendship(Session, u1, u2)
        f.accept(Session)
        self.assertEqual(f.status, 1)

        f = (
            Session.query(Friendship)
            .filter(Friendship.friend_one == u1.username)
            .filter(Friendship.friend_two == u2.username)
            .first()
        )
        self.assertEqual(f.status, 1)


class TestFollow(unittest.TestCase):
    def test_create_follow(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Follow(Session, u1, u2)
        self.assertEqual(f.follower, u1.username)
        self.assertEqual(f.followed, u2.username)

        f = (
            Session.query(Follow)
            .filter(Follow.follower == u1.username)
            .filter(Follow.followed == u2.username)
            .first()
        )
        self.assertIsNotNone(f)

    def test_unfollow(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u1.follow(Session, u2)
        u1.unfollow(Session, u2)

        f = (
            Session.query(Follow)
            .filter(Follow.follower == u1.username)
            .filter(Follow.followed == u2.username)
            .first()
        )
        self.assertIsNone(f)

    def test_unfollow_fail_no_follow(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        with self.assertRaises(Exception):
            u1.unfollow(Session, u2)

    def test_reject(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        f = Friendship(Session, u1, u2)
        f.reject(Session)

        f = (
            Session.query(Friendship)
            .filter(Friendship.friend_one == u1.username)
            .filter(Friendship.friend_two == u2.username)
            .first()
        )
        self.assertIsNone(f)

    def test_get_followers(self):
        u1 = User(Session, random_username(), "PASS", random_email(), "SOME BIO")
        u2 = User(Session, random_username(), "PASS", random_email(), "SOME BIO2")

        u2.follow(Session, u1)

        self.assertEqual(u1.get_followers(Session), [u2.username])
        self.assertEqual(u1.get_following(Session), [])
        self.assertEqual(u2.get_followers(Session), [])
        self.assertEqual(u2.get_following(Session), [u1.username])


def main():
    unittest.main()


if __name__ == "__main__":
    main()
