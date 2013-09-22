from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://localhost:5432/goattower', echo=True)

Base = declarative_base()


class Actor(Base):

    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('actor.id'))
    is_player = Column(Boolean)

    parent = relationship('Actor', primaryjoin=('Actor.parent_id == Actor.id'),
                          uselist=False)

    def __init__(self, name, is_player=False):
        self.name = name
        self.is_player = is_player


class ActorAttribute(Base):

    __tablename__ = 'actorattribute'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    key = Column(String)
    value = Column(String)

    def __init__(self, actor_id, key, value=None):
        self.actor_id = actor_id
        self.key = key
        self.value = value


class Command(Base):
    __tablename__ = 'command'

    id = Column(Integer, primary_key=True)
    regex = Column(String)
    actor_id = Column(Integer, ForeignKey('actor.id'))

    def __init__(self, regex, actor_id, code_id):
        self.regex = regex
        self.actor_id = actor_id
        self.code_id = code_id


class Code(Base):
    __tablename__ = 'code'

    id = Column(Integer, primary_key=True)
    command_id = Column(Integer, ForeignKey('command.id'))
    method = Column(String)
    args = Column(String)

    def __init__(self, command_id, method, args):
        self.command_id = command_id
        self.method = method
        self.args = args


Base.metadata.create_all(engine)
