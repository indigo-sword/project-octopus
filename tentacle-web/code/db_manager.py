from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

engine = create_engine("sqlite:///tentacle-web.sqlite")
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()
Base.query = Session.query_property()


# this method will only run once, when the database is created
def init_db():
    import node, user, path

    Base.metadata.create_all(bind=engine)
    Session.commit()
