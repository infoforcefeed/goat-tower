import api
import re
from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy.sql import bindparam
from models import engine, Actor, Code, Command

# start session
Session = sessionmaker(bind=engine)
session = Session()

# compile queries
command_queries = {}
command_queries['character'] = \
    session.query(Command).\
    filter(Command.actor_id == bindparam('actor_id'))

command_queries['children'] = \
    session.query(Actor, Command).\
    filter(Actor.id == bindparam('actor_id')).\
    join(Actor.parent, aliased=True).\
    filter(Command.actor_id == Actor.id)

location = aliased(Actor)
command_queries['location'] = \
    session.query(Command).\
    join(location).\
    join(Actor, location.id == Actor.parent_id).\
    filter(Actor.id == bindparam('actor_id'))

location = aliased(Actor)
children = aliased(Actor)
command_queries['location_children'] = \
    session.query(Command).\
    join(location).\
    join(Actor, location.id == Actor.parent_id).\
    join(children, location.id == children.parent_id).\
    filter(Actor.id == bindparam('actor_id')).\
    filter(Command.actor_id == children.id)

command_precedence = ['character', 'children', 'location', 'location_children']


def handle_text(actor_id, text):
    # TODO: have some game commands
    # For now assume all text is intended for a game object
    for command_type in command_precedence:
        commands = command_queries[command_type].params(actor_id=actor_id).all()
        matches = []
        for command in commands:
            regex = re.compile(command.regex)
            if regex.match(text):
                matches.append(command)

        if len(matches) > 1:
            print 'Ambiguous command'
            return
        elif len(matches) == 1:
            run_code(actor_id, command)
            return

    print 'Huh?'


def run_code(actor_id, command):
    for code in command.code:
        api.run_method(actor_id, code.method, code.args)
