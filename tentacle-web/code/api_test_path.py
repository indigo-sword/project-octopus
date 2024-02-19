import requests
import random
import string

url = f"http://localhost:7809/"

import unittest
import os


def random_email():
    return (
        "".join(random.choice(string.ascii_letters) for _ in range(10)) + "@gmail.com"
    )


def random_username():
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


def new_user():
    session = requests.Session()
    u = random_username()
    session.post(
        url + "create_user",
        data={
            "username": u,
            "password": "PASS",
            "email": random_email(),
            "bio": "BIO",
        },
    )

    return u, session


def login(u: str, session: requests.Session):
    session.post(url + "login", data={"username": u, "password": "PASS"})


def new_path(u: str, session: requests.Session):
    r = session.post(
        url + "create_path",
        data={
            "username": u,
            "title": "TITLE",
            "description": "DESCRIPTION",
        },
    )
    return r.json()["path_id"]


def new_node(u: str, session: requests.Session):
    with open("files/test.txt", "wb") as f:
        f.write(b"node file")

    with open("files/test.txt", "rb") as f:
        response = session.post(
            url + "create_node",
            data={
                "username": u,
                "description": "some description",
                "title": "some title",
            },
            files={"file": f},
        )

    return response.json()["node_id"]


def add_to_path(u: str, session: requests.Session, p: str, n: str, pos: int):
    session.post(
        url + "add_to_path",
        data={
            "username": u,
            "path_id": p,
            "node_id": n,
            "position": pos,
        },
    )


class TestApiPath(unittest.TestCase):
    def test_create_path(self):
        u, session = new_user()
        login(u, session)

        with self.subTest("create path"):
            r = session.post(
                url + "create_path",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                },
            )
            p = r.json()["path_id"]
            self.assertEqual(r.status_code, 201)
            self.assertEqual(r.json()["message"], "path created")

        with self.subTest("create path no title"):
            r = session.post(
                url + "create_path",
                data={
                    "username": u,
                    "description": "DESCRIPTION",
                },
            )
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()["message"], "no title parameter")

        with self.subTest("create path no description"):
            r = session.post(
                url + "create_path",
                data={
                    "username": u,
                    "title": "TITLE",
                },
            )
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()["message"], "no description parameter")

        with self.subTest("create path no user"):
            r = session.post(
                url + "create_path",
                data={
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                },
            )
            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()["message"], "no username parameter")

        with self.subTest("create path user not logged in"):
            session2 = requests.Session()
            r = session2.post(
                url + "create_path",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                },
            )
            self.assertEqual(r.status_code, 401)
            self.assertEqual(r.json()["message"], "user not logged in")

        with self.subTest("create path wrong user for request"):
            r = session.post(
                url + "create_path",
                data={
                    "username": "someone_else",
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                },
            )
            self.assertEqual(r.status_code, 401)
            self.assertEqual(r.json()["message"], "wrong user for request")

    def test_add_to_path(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)
        n1 = new_node(u, session)
        n2 = new_node(u, session)

        with self.subTest("add to path"):
            r = session.post(
                url + "add_to_path",
                data={
                    "username": u,
                    "path_id": p,
                    "node_id": n1,
                    "position": 0,
                },
            )
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()["message"], "node added to path")

        with self.subTest("add to path on position zero when there is a zero already"):
            r = session.post(
                url + "add_to_path",
                data={
                    "username": u,
                    "path_id": p,
                    "node_id": n2,
                    "position": 0,
                },
            )
            self.assertEqual(r.status_code, 400)
            self.assertEqual(
                r.json()["message"],
                "invalid position - path already has node in position zero",
            )

    def test_get_path(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)
        n1 = new_node(u, session)
        n2 = new_node(u, session)

        add_to_path(u, session, p, n1, 0)
        add_to_path(u, session, p, n2, 1)

        with self.subTest("get path"):
            response = session.get(url + "get_path", data={"path_id": p})
            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.json()["message"], "path info")
            self.assertEqual(response.json()["path"]["user_id"], u)
            self.assertEqual(response.json()["path"]["title"], "TITLE")
            self.assertEqual(response.json()["path"]["description"], "DESCRIPTION")
            self.assertEqual(response.json()["path"]["playcount"], 0)
            self.assertEqual(response.json()["path"]["num_ratings"], 0)
            self.assertEqual(response.json()["path"]["rating"], 0)
            self.assertEqual(response.json()["path"]["node_sequence"], [n1, n2])
            self.assertEqual(response.json()["path"]["positions"], [0, 1])

        with self.subTest("get path no path_id"):
            response = session.get(url + "get_path")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no path_id parameter")

        with self.subTest("get path not found"):
            response = session.get(url + "get_path", data={"path_id": "not_found"})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "path not found")

    def test_create_path_from_nodes(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)
        n1 = new_node(u, session)
        n2 = new_node(u, session)

        with self.subTest("create path from nodes"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                    "node_ids": [n1, n2],
                    "positions": [0, 1],
                },
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json()["message"], "path created")

        with self.subTest("create path from nodes no title"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "description": "DESCRIPTION",
                    "node_ids": [n1, n2],
                    "positions": [0, 1],
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no title parameter")

        with self.subTest("create path from nodes no description"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "title": "TITLE",
                    "node_ids": [n1, n2],
                    "positions": [0, 1],
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest("create path non-existent node"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                    "node_ids": ["non_existent", n2],
                    "positions": [0, 1],
                },
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

        with self.subTest("create path position is not a number"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                    "node_ids": [n1, n2],
                    "positions": ["a", "b"],
                },
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["message"],
                "node_ids and positions must be the same length",
            )

        with self.subTest("create path invalid position"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                    "node_ids": [n1, n2],
                    "positions": [-1, 0],
                },
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["message"],
                f"path not created. try again. node with id {n1} in position -1 had the following problem: invalid position - negative",
            )

        with self.subTest("create path not logged in"):
            response = requests.post(
                url + "create_path_from_nodes",
                data={
                    "username": u,
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                    "node_ids": [n1, n2],
                    "positions": [0, 1],
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("create path wrong user for request"):
            response = session.post(
                url + "create_path_from_nodes",
                data={
                    "username": "someone_else",
                    "title": "TITLE",
                    "description": "DESCRIPTION",
                    "node_ids": [n1, n2],
                    "positions": [0, 1],
                },
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

    def test_update_path_playcount(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)

        with self.subTest("update path playcount"):
            response = session.post(url + "update_path_playcount", data={"path_id": p})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "path playcount updated")

            response = session.get(url + "get_path", data={"path_id": p})

            self.assertEqual(response.json()["path"]["playcount"], 1)

        with self.subTest("update path playcount no path_id"):
            response = session.post(url + "update_path_playcount")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no path_id parameter")

        with self.subTest("update path playcount not found"):
            response = session.post(
                url + "update_path_playcount", data={"path_id": "not_found"}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "path not found")

    def test_update_path_rating(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)

        with self.subTest("update path rating"):
            response = session.post(
                url + "update_path_rating",
                data={"path_id": p, "rating": 5, "username": u},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "path rating updated")

            response = session.get(url + "get_path", data={"path_id": p})

            self.assertEqual(response.json()["path"]["rating"], 5)

        with self.subTest("update path rating no path_id"):
            response = session.post(
                url + "update_path_rating", data={"rating": 5, "username": u}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no path_id parameter")

        with self.subTest("update path rating not found"):
            response = session.post(
                url + "update_path_rating",
                data={"path_id": "not_found", "rating": 5, "username": u},
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "path not found")

        with self.subTest("update path rating not a number"):
            response = session.post(
                url + "update_path_rating",
                data={"path_id": p, "rating": "not_a_number", "username": u},
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "rating is not an int")

        with self.subTest("update path rating out of range"):
            response = session.post(
                url + "update_path_rating",
                data={"path_id": p, "rating": 11, "username": u},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()["message"], "rating must be between 0 and 10"
            )

        with self.subTest("update path rating not logged in"):
            response = requests.post(
                url + "update_path_rating",
                data={"path_id": p, "rating": 5, "username": u},
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("update path rating wrong user for request"):
            response = session.post(
                url + "update_path_rating",
                data={"path_id": p, "rating": 5, "username": "someone_else"},
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

    def test_update_path_title(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)

        with self.subTest("update path title"):
            response = session.post(
                url + "update_path_title",
                data={"path_id": p, "title": "NEW_TITLE", "username": u},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "path title updated")

            response = session.get(url + "get_path", data={"path_id": p})

            self.assertEqual(response.json()["path"]["title"], "NEW_TITLE")

        with self.subTest("update path title no path_id"):
            response = session.post(
                url + "update_path_title", data={"title": "NEW_TITLE", "username": u}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no path_id parameter")

        with self.subTest("update path title not found"):
            response = session.post(
                url + "update_path_title",
                data={"path_id": "not_found", "title": "NEW_TITLE", "username": u},
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "path not found")

        with self.subTest("update path title no title"):
            response = session.post(
                url + "update_path_title", data={"path_id": p, "username": u}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no title parameter")

        with self.subTest("update path title not logged in"):
            response = requests.post(
                url + "update_path_title",
                data={"path_id": p, "title": "NEW_TITLE", "username": u},
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("update path title wrong user for request"):
            response = session.post(
                url + "update_path_title",
                data={"path_id": p, "title": "NEW_TITLE", "username": "someone_else"},
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

    def test_update_path_description(self):
        u, session = new_user()
        login(u, session)

        p = new_path(u, session)

        with self.subTest("update path description"):
            response = session.post(
                url + "update_path_description",
                data={"path_id": p, "description": "NEW_DESCRIPTION", "username": u},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "path description updated")

            response = session.get(url + "get_path", data={"path_id": p})

            self.assertEqual(response.json()["path"]["description"], "NEW_DESCRIPTION")

        with self.subTest("update path description no path_id"):
            response = session.post(
                url + "update_path_description",
                data={"description": "NEW_DESCRIPTION", "username": u},
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no path_id parameter")

        with self.subTest("update path description not found"):
            response = session.post(
                url + "update_path_description",
                data={
                    "path_id": "not_found",
                    "description": "NEW_DESCRIPTION",
                    "username": u,
                },
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "path not found")

        with self.subTest("update path description no description"):
            response = session.post(
                url + "update_path_description", data={"path_id": p, "username": u}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest("update path description not logged in"):
            response = requests.post(
                url + "update_path_description",
                data={"path_id": p, "description": "NEW_DESCRIPTION", "username": u},
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("update path description wrong user for request"):
            response = session.post(
                url + "update_path_description",
                data={
                    "path_id": p,
                    "description": "NEW_DESCRIPTION",
                    "username": "someone_else",
                },
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

    def test_get_user_paths(self):
        u, session = new_user()
        login(u, session)

        p1 = new_path(u, session)
        p2 = new_path(u, session)

        with self.subTest("get user paths"):
            response = session.get(url + "get_user_paths", data={"username": u})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "user paths")
            self.assertEqual(response.json()["paths"][0]["path_id"], p1)
            self.assertEqual(response.json()["paths"][1]["path_id"], p2)

        with self.subTest("get user paths no username"):
            response = session.get(url + "get_user_paths")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("get user paths not found"):
            response = session.get(
                url + "get_user_paths", data={"username": "not_found"}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "user not found")

    def test_get_node_paths(self):
        u, session = new_user()
        login(u, session)

        p1 = new_path(u, session)
        p2 = new_path(u, session)

        n = new_node(u, session)

        add_to_path(u, session, p1, n, 0)
        add_to_path(u, session, p2, n, 0)

        with self.subTest("get node paths"):
            response = session.get(url + "get_node_paths", data={"node_id": n})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "node paths")
            self.assertTrue(p1 in [p["path_id"] for p in response.json()["paths"]])
            self.assertTrue(p2 in [p["path_id"] for p in response.json()["paths"]])
            self.assertTrue(len(response.json()["paths"]) == 2)

        with self.subTest("get node paths no node_id"):
            response = session.get(url + "get_node_paths")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("get node paths not found"):
            response = session.get(
                url + "get_node_paths", data={"node_id": "not_found"}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
