from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
sql_connection_default = 'sqlite:///modules///models///data///sample.sqllite3'

# With区でSessionを管理する
# http://momijiame.tumblr.com/post/30241416710/python-%E3%81%AE-with-%E6%96%87%E3%81%A7-sqlalchemy-%E3%81%AE%E3%82%BB%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B
class SessionFactory(object):
    def __init__(self, sql_connection, echo):
        self.engine = create_engine(sql_connection, echo=echo)
        base.metadata.create_all(self.engine)
    
    def create(self):
        session = sessionmaker(bind=self.engine)
        return session()

class SessionContext(object):
    def __init__(self, session):
        self.session = session
    
    def __enter__(self):
        return self.session
    
    def __exit__(self, ex_type, ex_value, traceback):
        self.session.flush()
        if ex_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

class SessionContextFactory(object):
    def __init__(self ,sql_connection=sql_connection_default, echo=True):
        self.session_factory = SessionFactory(sql_connection, echo)
    
    def create(self):
        return SessionContext(self.session_factory.create())

# define table
class User(base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)
