from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

engine = create_engine('sqlite:///tentacle-web.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# this method will only run once, when the database is created
def init_db():
    import node, level, user
    Base.metadata.create_all(bind=engine)
    db_session.commit()