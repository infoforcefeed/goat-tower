import json
from sqlalchemy.orm import sessionmaker
from models import engine, Actor, PlayerText


def run_method(actor_id, method_name, args_string):
    args = json.loads(args_string)
    args = map(lambda x: actor_id if x == '@origin' else x, args)
    getattr(api, method_name)(*args)


class API(object):

    def __init__(self):
        # start session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def send_text(self, actor_id, text):
        actor = self.session.query(Actor).get(actor_id)
        if actor.is_player:
            self.session.add(PlayerText(actor_id, text))
            self.session.commit()

    def update_location(self, actor_id, location_id):
        actor = self.session.query(Actor).get(actor_id)
        actor.parent_id = location_id
        self.session.commit()

api = API()
