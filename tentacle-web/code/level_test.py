from level import Level
from user import User
from db_manager import db_session

def main():
    u = User(db_session, "USERNAME", "PASSWORD", "EMAIL", "BIO")
    l = Level(db_session, u, b'TEST PASS')

    # query levels for l
    r = db_session.query(Level).filter(Level.id == l.id).first()
    print(r)

    # read file
    with open(r.get_file_path(), 'r') as f:
        print("FILE READ:")
        print(f.read()) # this should be a level already

if __name__ == "__main__":
    main()