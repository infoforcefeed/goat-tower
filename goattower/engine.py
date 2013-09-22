import api
import re
from sqlalchemy.orm import sessionmaker
from models import engine, Base, Code, Command


def handle_text(actor_id, text):   
    # start session
    Session = sessionmaker(bind=engine)
    session = Session()

    # look for commands on current character
    commands = session.query(Command).filter(Command.actor_id == actor_id).all()
    # TODO: handle multiple matches
    for command in commands:
        regex = re.compile(command.regex)
        match = regex.match(text)
        if regex.match:
            run_code(actor_id, command.id)

    # TODO: go past character


def run_code(actor_id, command_id):
    codes = session.query(Code).filter(Command.id == command_id).all()
    for code in codes:
        api.run_method(code.actor_id, code.method, code.args)
