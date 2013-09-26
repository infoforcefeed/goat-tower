import json
import sys
from sqlalchemy.orm import sessionmaker
import models

def load(data):
    from models import engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for actor in data:
        new_actor = models.Actor(name=actor['name'])
        new_actor.id = actor['id']
        new_actor.is_player = actor.get('is_player', False)
        new_actor.parent_id = actor.get('parent_id', None)
        session.add(new_actor)

        for command in actor.get('commands', []):
            commands = []
            for regex in command['regex']:
                new_command = models.Command(
                    regex=regex,
                    actor_id=new_actor.id)
                commands.append(new_command)
                session.add(new_command)

            code = []
            for command in command['code']:
                method, args = command.popitem()
                new_code = models.Code(method, json.dumps(args))
                code.append(new_code)
                session.add(new_code)
            
            for command in commands:
                for cd in code:
                    command.code.append(cd)

    session.commit()

def load_json(json_str):
    load(json.loads(json_str))

def load_yaml(yaml_str):
    import yaml
    load(yaml.load(yaml_str))

parser_map = {
    'yaml': load_yaml,
    'json': load_json,
}

def main():
    import argparse # TODO: eventually..
    argparse

    data_file = sys.argv[1]
    file_type = sys.argv[2]
    parser = parser_map.get(file_type, None)
    if parser:
        parser(open(data_file).read())
    else:
        print 'File type "{}" not supported'.format(file_type)
        sys.exit(1)

if __name__ == '__main__':
    main()
