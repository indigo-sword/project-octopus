from path import Path, path_node_association
from db_manager import db_session
from node import Node
from level import Level
from user import User

u = User(db_session, "NAME", "PASS", "EMAIL", "BIO")
print("===== USER =====", u.id)

def new_path():
    p = Path(db_session, u, "DESCRIPTION")
    print("saved!", p.id)
    return p

def test_query_path(path_id: str):
    p = db_session.query(Path).filter(Path.id == f"{path_id}").first()
    print("===== QUERIED =====", p.id)

def test_add_node(p: Path, n: Node):
    p.add_node(n, db_session)
    print("===== ADDED NODE =====", n.id)

def main():
    p = new_path()
    test_query_path(p.id)

    l = Level(db_session, u, b'')
    n = Node(db_session, l, u, "test")
    test_add_node(p, n)

    n = Node(db_session, l, u, "test")
    test_add_node(p, n)

    n = Node(db_session, l, u, "test")
    test_add_node(p, n)

    print("===== NODE SEQUENCE =====")
    print(p.get_node_sequence(db_session))

    p2 = new_path()
    test_add_node(p2, n) # should work

    print("===== NODE SEQUENCE =====")
    print(p2.get_node_sequence(db_session))

    test_add_node(p, n) # should not work

if __name__ == "__main__":
    main()