from user import User
from db_manager import db_session

def main():
    u = User(db_session, "TEST", "PASS", "EMAIL", "SOME BIO")
    print(u.id)
    # query users for u
    r = db_session.query(User).filter(User.id == u.id).first()
    print(u.id, r.id, u.id == r.id, u.email, r.email, u.email == r.email, u.password, r.password, u.password == r.password, u.username, r.username, u.username == r.username)

if __name__ == "__main__":
    main()