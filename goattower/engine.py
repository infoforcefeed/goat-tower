import re
from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy.sql import bindparam
from models import engine, Actor, Command, PlayerText
from api import api, run_method

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

    #TODO: FUCKING COMMENT
    for command_type in command_precedence:
        commands = command_queries[command_type].params(actor_id=actor_id).all()
        matches = []
        for command in commands:
            regex = re.compile(command.regex).match
            match = regex(text)
            if match:
                matches.append((command, match))

        if len(matches) > 1:
            # Too many matches, ambiguous
            api.send_text(actor_id, 'Ambiguous command')
            return
        elif len(matches) == 1:
            # Exactly one match, respond
            run_code(actor_id, *matches[0])
            return

    class fuck(object):
        def groupdict(self):
            return

    # We have no matches, just shout at user
    api.send_text(actor_id, 'Huh?', fuck())


def get_text(actor_id):
    text_objs = session.query(PlayerText).\
        filter(PlayerText.actor_id == actor_id)
    text = []
    for text_obj in text_objs:
        text.append(text_obj.text)
        session.delete(text_obj)
    session.commit()
    return text

def run_code(actor_id, command, match):
    context = {
        'origin': actor_id,
        'match': match.groupdict()
    }
    for code in command.code:
        run_method(code.method, code.args, context)
