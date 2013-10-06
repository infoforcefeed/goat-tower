import json
from jinja2 import Template
from sqlalchemy.orm import sessionmaker
from models import engine, Actor, PlayerText


def run_method(method_name, args_string, context):
    template = Template(args_string)
    args_json_string = template.render(context)
    getattr(api, method_name)(*json.loads(args_json_string))


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
