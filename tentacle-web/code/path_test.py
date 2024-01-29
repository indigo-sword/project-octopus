from path import Path, path_node_association
from db_manager import db_session
from node import Node
from level import Level
from user import User

def new_path():
    p = Path()
    p.save(db_session)
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

    n = Node(Level(0), User("joao", "idk", "jpireshe@nd.edu"), "test")
    test_add_node(p, n)

    n = Node(Level(0), User("joao", "idk", "jpireshe@nd.edu"), "test")
    test_add_node(p, n)

    n = Node(Level(0), User("joao", "idk", "jpireshe@nd.edu"), "test")
    test_add_node(p, n)

    print("===== NODE SEQUENCE =====")
    print(p.get_node_sequence(db_session))

if __name__ == "__main__":
    main()