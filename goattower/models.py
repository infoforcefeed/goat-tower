from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
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


class CodeCommandMap(Base):
    __tablename__ = 'codecommandmap'
    code_id = Column(Integer, ForeignKey('code.id'), primary_key=True)
    command_id = Column(Integer, ForeignKey('command.id'), primary_key=True)
    code = relationship('Code', backref='commmand_assocs')
    command = relationship('Command', backref='code_assocs')

    def __init__(self, code=None, command=None):
        self.code = code
        self.command = command


class Command(Base):
    __tablename__ = 'command'

    id = Column(Integer, primary_key=True)
    regex = Column(String)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    code = association_proxy('code_assocs', 'code')

    def __init__(self, regex, actor_id):
        self.regex = regex
        self.actor_id = actor_id


class Code(Base):
    __tablename__ = 'code'

    id = Column(Integer, primary_key=True)
    method = Column(String)
    args = Column(String)
    commands = association_proxy('command_assocs', 'command')

    def __init__(self, method, args):
        self.method = method
        self.args = args


Base.metadata.create_all(engine)
