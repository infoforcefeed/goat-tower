import api
import re
from sqlalchemy.orm import aliased, sessionmaker
from models import engine, Actor, Code, Command

# start session
Session = sessionmaker(bind=engine)
session = Session()

def handle_text(actor_id, text):

    # TODO: handle multiple matches
    # TODO: remove copypasta

    # Look for commands on current character
    commands = session.query(Command).filter(Command.actor_id == actor_id).all()
    for command in commands:
        regex = re.compile(command.regex)
        match = regex.match(text)
        if match:
            run_code(actor_id, command.id)

    # Children of character
    commands = session.query(Actor, Command).\
        filter(Actor.id == actor_id).\
        join(Actor.parent, aliased=True).\
        filter(Command.actor_id == Actor.id).all()
    for command in commands:
        regex = re.compile(command.regex)
        match = regex.match(text)
        if match:
            run_code(actor_id, command.id)

    # Location
    location = aliased(Actor)
    commands = session.query(Command).\
        join(location).\
        join(Actor, location.id == Actor.parent_id).\
        filter(Actor.id == actor_id).all()
    for command in commands:
        regex = re.compile(command.regex)
        match = regex.match(text)
        if match:
            run_code(actor_id, command.id)

    # Things at current location
    # TODO

def run_code(actor_id, command_id):
    codes = session.query(Code).filter(Command.id == command_id).all()
    for code in codes:
        api.run_method(actor_id, code.method, code.args)
