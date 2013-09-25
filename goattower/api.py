import json


def run_method(actor_id, method_name, args_string):
    args = json.loads(args_string)
    args = map(lambda x: actor_id if x == '@origin' else x, args)
    getattr(api, method_name)(*args)


class API(object):

    def send_text(self, actor_id, text):
        print 'send_text: {} - {}'.format(actor_id, text)

    def update_location(self, actor_id, location_id):
        print 'update_location: {} - {}'.format(actor_id, location_id)

api = API()
