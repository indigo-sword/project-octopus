from level import Level
from db_manager import db_session

def main():
    l = Level(db_session, 10)
    # query levels for l
    r = db_session.query(Level).filter(Level.id == l.id).first()
    print(l.id, r.id, l.id == r.id, l.level, r.level, l.level == r.level)

if __name__ == "__main__":
    main()