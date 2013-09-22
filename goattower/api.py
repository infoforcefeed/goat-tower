import json


def run_method(actor_id, method_name, args_string):
    args = json.loads(args_string)
    args = map(lambda x: actor_id if x == '@origin' else x, args)
    getattr(api, method_name)(*args)


class API(object):
    pass

api = API()
