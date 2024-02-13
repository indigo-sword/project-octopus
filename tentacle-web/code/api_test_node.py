import requests
import random
import string

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
            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
            
            with open("files/test.txt", "rb") as f:
                response = session.post(url + "create_node", data={
                    "username": u,
                    "description": "some description",
                }, files={"file": f})
                
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json()["message"], "node created")
                self.assertTrue("node_id" in response.json())
                i = response.json()["node_id"]

            os.remove("files/test.txt")

            with open("../levels/" + i + ".level", "rb") as f:
                self.assertEqual(f.read(), b"THIS TEST HAS PASSED! 11")

        with self.subTest(msg="create node no username"):
            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()

            f = open("files/test.txt", "rb")

            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            response = session.post(url + "create_node", data={
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("files/test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest(msg="create node no description"):
            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()

            f = open("files/test.txt", "rb")

            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            response = session.post(url + "create_node", data={
                "username": u,
            }, files={"file": f})

            f.close()

            os.remove("files/test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest(msg="create node no file"):
            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no file parameter")

        with self.subTest(msg="create node no file data"):
            with open("files/test.txt", "wb") as f:
                f.close()

            f = open("files/test.txt", "rb")

            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("files/test.txt")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no file data")

        with self.subTest(msg="user does not exist"):
            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()
            
            f = open("files/test.txt", "rb")

            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            response = session.post(url + "create_node", data={
                "username": "nonexistentuser",
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("files/test.txt")

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest(msg="user not logged in"):
            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
                f.close()
            
            f = open("files/test.txt", "rb")

            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})

            f.close()

            os.remove("files/test.txt")

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

    def test_change_node_description(self):
        with self.subTest("change node description"):
            session = requests.Session()

            u = random_username()
            session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")
            
            with open("files/test.txt", "rb") as f:
                response = session.post(url + "create_node", data={
                    "username": u,
                    "description": "some description",
                }, files={"file": f})
                nid = response.json()["node_id"]

            os.remove("files/test.txt")

            response = session.post(url + "change_node_description", data={
                "username": u,
                "node_id": nid,
                "description": "new description"
            })
        
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "node updated")

        with self.subTest("change node description no username"):
            response = session.post(url + "change_node_description", data={
                "node_id": nid,
                "description": "new description"
            })
        
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("change node description no node_id"):
            response = session.post(url + "change_node_description", data={
                "username": u,
                "description": "new description"
            })
        
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("change node description no description"):
            response = session.post(url + "change_node_description", data={
                "username": u,
                "node_id": nid,
            })
        
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest("change node description no node"):
            response = session.post(url + "change_node_description", data={
                "username": u,
                "node_id": "nonexistentnode",
                "description": "new description"
            })
        
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

        with self.subTest("change node description wrong user"):
            response = session.post(url + "change_node_description", data={
                "username": "nonexistentuser",
                "node_id": nid,
                "description": "new description"
            })
        
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest("change node description user does not own node"):
            sessionOne = requests.Session()
            sessionTwo = requests.Session()

            uOne = random_username()
            uTwo = random_username()

            sessionOne.post(url + "create_user", data={
                "username": uOne,
                "password": "password_4_joao",
                "email": random_email()
            })

            sessionTwo.post(url + "create_user", data={
                "username": uTwo,
                "password": "password_4_joao",
                "email": random_email()
            })

            sessionOne.post(url + "login", data={
                "username": uOne,
                "password": "password_4_joao"
            })

            sessionTwo.post(url + "login", data={
                "username": uTwo,
                "password": "password_4_joao"
            })

            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")

            with open("files/test.txt", "rb") as f:
                response = sessionOne.post(url + "create_node", data={
                    "username": uOne,
                    "description": "some description",
                }, files={"file": f})
                nid = response.json()["node_id"]

            os.remove("files/test.txt")

            response = sessionTwo.post(url + "change_node_description", data={
                "username": uTwo,
                "node_id": nid,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user does not own this node")

        with self.subTest("change node description user not logged in"):
            session = requests.Session()
            response = session.post(url + "change_node_description", data={
                "username": u,
                "node_id": nid,
                "description": "new description"
            })
        
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

    def test_get_node(self):
        # create a node
        session = requests.Session()
        u = random_username()
        session.post(url + "create_user", data={
            "username": u,
            "password": "password_4_joao",
            "email": random_email()
        })

        session.post(url + "login", data={
            "username": u,
            "password": "password_4_joao"
        })

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})
            nid = response.json()["node_id"]
        
        with self.subTest("get node"):
            session = requests.Session()
            response = session.get(url + "get_node", data={
                "node_id": nid
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "node info")
            self.assertEqual(response.json()["description"], "some description")
            self.assertEqual(response.json()["num_ratings"], 0)
            self.assertEqual(response.json()["rating"], 0)
            self.assertEqual(response.json()["playcount"], 0)
            self.assertTrue("ts" in response.json())
            self.assertEqual(response.json()["user_id"], u)

        with self.subTest("get node no node_id"):
            response = session.get(url + "get_node")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("get node node does not exist"):
            response = session.get(url + "get_node", data={
                "node_id": "nonexistentnode"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

    def test_link_nodes(self):
        sessionOne = requests.Session()
        sessionTwo = requests.Session()

        uOne = random_username()
        uTwo = random_username()

        sessionOne.post(url + "create_user", data={
            "username": uOne,
            "password": "password_4_joao",
            "email": random_email()
        })

        sessionTwo.post(url + "create_user", data={
            "username": uTwo,
            "password": "password_4_joao",
            "email": random_email()
        })

        sessionOne.post(url + "login", data={
            "username": uOne,
            "password": "password_4_joao"
        })

        sessionTwo.post(url + "login", data={
            "username": uTwo,
            "password": "password_4_joao"
        })

        with self.subTest("link nodes"):
            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")

            with open("files/test.txt", "rb") as f:
                response = sessionOne.post(url + "create_node", data={
                    "username": uOne,
                    "description": "some description",
                }, files={"file": f})
                nidOne = response.json()["node_id"]

            with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")

            with open("files/test.txt", "rb") as f:
                response = sessionTwo.post(url + "create_node", data={
                    "username": uTwo,
                    "description": "some description",
                }, files={"file": f})
                nidTwo = response.json()["node_id"]

            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "nodes linked")

        with self.subTest("link nodes no username"):
            response = sessionOne.post(url + "link_nodes", data={
                "origin_id": nidOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("link nodes no origin_id"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no origin_id parameter")
        
        with self.subTest("link nodes no destination_id"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no destination_id parameter")
        
        with self.subTest("link nodes no description"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidTwo,
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest("link nodes no origin node"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": "nonexistentnode",
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "origin node not found")

        with self.subTest("link nodes no destination node"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": "nonexistentnode",
                "description": "some description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "destination node not found")

        with self.subTest("link nodes nodes already linked"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "nodes are already linked.")

        with self.subTest("link nodes user does not own origin node"):
            response = sessionTwo.post(url + "link_nodes", data={
                "username": uTwo,
                "origin_id": nidOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user does not own the origin node")

        with self.subTest("link nodes node link to itself"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidOne,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "cannot link node to itself")

        with open("files/test.txt", "wb") as f:
                f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = sessionTwo.post(url + "create_node", data={
                "username": uTwo,
                "description": "some description",
                "is_initial": "true",
            }, files={"file": f})
            nidThree = response.json()["node_id"]

        with self.subTest("link nodes to initial node"):
            response = sessionOne.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidThree,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "cannot link to initial node")

        with self.subTest("link nodes user not logged in"):
            session = requests.Session()
            response = session.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        with self.subTest("link nodes wrong user"):
            session = requests.Session()
            u = random_username()
            response = session.post(url + "create_user", data={
                "username": u,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = session.post(url + "login", data={
                "username": u,
                "password": "password_4_joao"
            })

            response = session.post(url + "link_nodes", data={
                "username": uOne,
                "origin_id": nidOne,
                "destination_id": nidTwo,
                "description": "some description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        os.remove("files/test.txt")

    def test_get_next_links(self):
        sessionOne = requests.Session()
        sessionTwo = requests.Session()

        uOne = random_username()
        uTwo = random_username()

        sessionOne.post(url + "create_user", data={
            "username": uOne,
            "password": "password_4_joao",
            "email": random_email()
        })

        sessionTwo.post(url + "create_user", data={
            "username": uTwo,
            "password": "password_4_joao",
            "email": random_email()
        })

        sessionOne.post(url + "login", data={
            "username": uOne,
            "password": "password_4_joao"
        })

        sessionTwo.post(url + "login", data={
            "username": uTwo,
            "password": "password_4_joao"
        })

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = sessionOne.post(url + "create_node", data={
                "username": uOne,
                "description": "some description",
            }, files={"file": f})
            nidOne = response.json()["node_id"]

            f.seek(0)

            response = sessionTwo.post(url + "create_node", data={
                "username": uTwo,
                "description": "some description",
            }, files={"file": f})
            nidTwo = response.json()["node_id"]

            f.seek(0)

            response = sessionTwo.post(url + "create_node", data={
                "username": uTwo,
                "description": "some description",
            }, files={"file": f})
            nidThree = response.json()["node_id"]

        response = sessionOne.post(url + "link_nodes", data={
            "username": uOne,
            "origin_id": nidOne,
            "destination_id": nidTwo,
            "description": "link from node one to node two"
        })

        response = sessionOne.post(url + "link_nodes", data={
            "username": uOne,
            "origin_id": nidOne,
            "destination_id": nidThree,
            "description": "link from node one to node three"
        })

        with self.subTest("get next links"):
            response = sessionOne.get(url + "get_next_links", data={
                "node_id": nidOne
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "next links")
            self.assertEqual(len(response.json()["next_links"]), 2)
            self.assertEqual(response.json()["next_links"][0]["description"], "link from node one to node two")
            self.assertEqual(response.json()["next_links"][0]["destination_id"], nidTwo)
            
            self.assertEqual(response.json()["next_links"][1]["description"], "link from node one to node three")
            self.assertEqual(response.json()["next_links"][1]["destination_id"], nidThree)

        with self.subTest("get next links no node_id"):
            response = sessionOne.get(url + "get_next_links")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("get next links node does not exist"):
            response = sessionOne.get(url + "get_next_links", data={
                "node_id": "nonexistentnode"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

    def test_get_previous_links(self):
        sessionOne = requests.Session()
        sessionTwo = requests.Session()

        uOne = random_username()
        uTwo = random_username()

        sessionOne.post(url + "create_user", data={
            "username": uOne,
            "password": "password_4_joao",
            "email": random_email()
        })

        sessionTwo.post(url + "create_user", data={
            "username": uTwo,
            "password": "password_4_joao",
            "email": random_email()
        })

        sessionOne.post(url + "login", data={
            "username": uOne,
            "password": "password_4_joao"
        })

        sessionTwo.post(url + "login", data={
            "username": uTwo,
            "password": "password_4_joao"
        })

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = sessionOne.post(url + "create_node", data={
                "username": uOne,
                "description": "some description",
            }, files={"file": f})
            nidOne = response.json()["node_id"]

            f.seek(0)

            response = sessionTwo.post(url + "create_node", data={
                "username": uTwo,
                "description": "some description",
            }, files={"file": f})
            nidTwo = response.json()["node_id"]

            f.seek(0)

            response = sessionTwo.post(url + "create_node", data={
                "username": uTwo,
                "description": "some description",
            }, files={"file": f})
            nidThree = response.json()["node_id"]

        response = sessionTwo.post(url + "link_nodes", data={
            "username": uTwo,
            "origin_id": nidTwo,
            "destination_id": nidOne,
            "description": "link from node two to node one"
        })

        response = sessionTwo.post(url + "link_nodes", data={
            "username": uTwo,
            "origin_id": nidThree,
            "destination_id": nidOne,
            "description": "link from node three to node one"
        })

        with self.subTest("get previous links"):
            response = sessionOne.get(url + "get_previous_links", data={
                "node_id": nidOne
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "previous links")
            self.assertEqual(len(response.json()["previous_links"]), 2)
            self.assertEqual(response.json()["previous_links"][0]["description"], "link from node two to node one")
            self.assertEqual(response.json()["previous_links"][0]["origin_id"], nidTwo)
            
            self.assertEqual(response.json()["previous_links"][1]["description"], "link from node three to node one")
            self.assertEqual(response.json()["previous_links"][1]["origin_id"], nidThree)

        with self.subTest("get previous links no node_id"):
            response = sessionOne.get(url + "get_previous_links")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("get previous links node does not exist"):
            response = sessionOne.get(url + "get_previous_links", data={
                "node_id": "nonexistentnode"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

    def test_update_playcount(self):
        # create a node
        session = requests.Session()
        u = random_username()
        session.post(url + "create_user", data={
            "username": u,
            "password": "password_4_joao",
            "email": random_email()
        })

        session.post(url + "login", data={
            "username": u,
            "password": "password_4_joao"
        })

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})
            nid = response.json()["node_id"]

        with self.subTest("update playcount"):
            response = session.post(url + "update_playcount", data={
                "node_id": nid
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "playcount updated")

            response = session.get(url + "get_node", data={
                "node_id": nid
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["playcount"], 1)

        with self.subTest("update playcount no node_id"):
            response = session.post(url + "update_playcount")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("update playcount node does not exist"):
            response = session.post(url + "update_playcount", data={
                "node_id": "nonexistentnode"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

        os.remove("files/test.txt")

    def test_update_rating(self):
        # create a node
        session = requests.Session()
        u = random_username()
        session.post(url + "create_user", data={
            "username": u,
            "password": "password_4_joao",
            "email": random_email()
        })

        session.post(url + "login", data={
            "username": u,
            "password": "password_4_joao"
        })

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})
            nid = response.json()["node_id"]

        with self.subTest("update rating"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": nid,
                "rating": 5
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "rating updated")

            response = session.get(url + "get_node", data={
                "username": u,
                "node_id": nid
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["rating"], 5)
            self.assertEqual(response.json()["num_ratings"], 1)

        with self.subTest("update rating no node_id"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "rating": 5
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("update rating no rating"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": nid
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no rating parameter")

        with self.subTest("update rating node does not exist"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": "nonexistentnode",
                "rating": 5
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

        with self.subTest("update rating user does not exist"):
            response = session.post(url + "update_rating", data={
                "username": "nonexistentuser",
                "node_id": nid,
                "rating": 5
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest("update rating is not a number"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": nid,
                "rating": "notanumber"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "rating is not a number")

        with self.subTest("update rating smaller than zero"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": nid,
                "rating": -1
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "rating must be between 0 and 10")

        with self.subTest("update rating greater than ten"):
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": nid,
                "rating": 11
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()["message"], "rating must be between 0 and 10")

        with self.subTest("update rating user not logged in"):
            session = requests.Session()
            response = session.post(url + "update_rating", data={
                "username": u,
                "node_id": nid,
                "rating": 5
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

        os.remove("files/test.txt")

    def test_update_node_description(self):
        # create a node
        session = requests.Session()
        u = random_username()
        session.post(url + "create_user", data={
            "username": u,
            "password": "password_4_joao",
            "email": random_email()
        })

        session.post(url + "login", data={
            "username": u,
            "password": "password_4_joao"
        })

        with open("files/test.txt", "wb") as f:
            f.write(b"THIS TEST HAS PASSED! 11")

        with open("files/test.txt", "rb") as f:
            response = session.post(url + "create_node", data={
                "username": u,
                "description": "some description",
            }, files={"file": f})
            nid = response.json()["node_id"]

        with self.subTest("update node description"):
            response = session.post(url + "update_node_description", data={
                "username": u,
                "node_id": nid,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["message"], "description updated")

            response = session.get(url + "get_node", data={
                "node_id": nid
            })

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["description"], "new description")
        
        with self.subTest("update node description no username"):
            response = session.post(url + "update_node_description", data={
                "node_id": nid,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no username parameter")

        with self.subTest("update node description no node_id"):
            response = session.post(url + "update_node_description", data={
                "username": u,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no node_id parameter")

        with self.subTest("update node description no description"):
            response = session.post(url + "update_node_description", data={
                "username": u,
                "node_id": nid,
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "no description parameter")

        with self.subTest("update node description no node"):
            response = session.post(url + "update_node_description", data={
                "username": u,
                "node_id": "nonexistentnode",
                "description": "new description"
            })

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()["message"], "node not found")

        with self.subTest("update node description user does not own node"):
            v = random_username()
            response = session.post(url + "create_user", data={
                "username": v,
                "password": "password_4_joao",
                "email": random_email()
            })

            response = session.post(url + "login", data={
                "username": v,
                "password": "password_4_joao"
            })

            response = session.post(url + "update_node_description", data={
                "username": v,
                "node_id": nid,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user does not own this node")

        with self.subTest("update node description wrong user"):
            response = session.post(url + "update_node_description", data={
                "username": "nonexistentuser",
                "node_id": nid,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "wrong user for request")

        with self.subTest("update node description user not logged in"):
            session = requests.Session()
            response = session.post(url + "update_node_description", data={
                "username": u,
                "node_id": nid,
                "description": "new description"
            })

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()["message"], "user not logged in")

def main():
    unittest.main()

if __name__ == "__main__":
    main()

