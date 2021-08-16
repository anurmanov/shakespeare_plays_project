import os
import pprint
from functools import wraps
from collections import namedtuple
import pymongo


def mongo_connection(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        uri = 'mongodb://{}:{}@{}:{}/?authSource=admin'.format(
            os.getenv('DB_USER'),
            os.getenv('DB_PASSWORD'),
            os.getenv('MONGO_HOST'),
            os.getenv('MONGO_EXTERNAL_PORT'),
        )
        client = pymongo.MongoClient(uri)
        result = f(client, *args, **kwargs)
        client.close()

        return result

    return wrapper


@mongo_connection
def find_most_popular_characters(client):
    db = client[os.getenv('DB_NAME')]
    plays = db.plays

    result = plays.aggregate(
        [
            {
                '$unwind': {
                    'path': '$acts',
                    'preserveNullAndEmptyArrays': True
                }
            },

            {
                '$unwind': {
                    'path': '$acts.scenes',
                    'preserveNullAndEmptyArrays': True
                }
            },

            {
                '$unwind': {
                    'path': '$acts.scenes.action',
                    'preserveNullAndEmptyArrays': True
                }
            },

            {
                '$set': {
                    'play': '$_id',
                    'character': {"$toUpper": "$acts.scenes.action.character"}
                }
            },

            {
                '$unset': [
                    'acts', '_id'
                ]
            },

            {
                '$group': {
                    '_id': '$character',
                    'character': {
                        '$first': '$character'
                    },
                    'plays': {
                        '$addToSet': '$play'
                    }
                }
            },

            {
                '$set': {
                    'acted_in_plays': {
                        '$size': '$plays'
                    }
                }
            },

            {
                '$unset': '_id'
            },

            {
                '$match': {
                    'acted_in_plays': {
                        '$gt': 1
                    }
                }
            },

            {
                '$sort': {
                    'acted_in_plays': -1
                }
            }
        ]
    )
    pprint.pprint(list(result))


@mongo_connection
def find_most_actioned_play(client):
    db = client[os.getenv('DB_NAME')]
    plays = db.plays

    result = plays.aggregate(
        [
            {
                '$unwind': {
                    'path': '$acts',
                    'preserveNullAndEmptyArrays': True
                }
            },

            {
                '$unwind': {
                    'path': '$acts.scenes'
                }
            },

            {
                '$set': {
                    'scene': '$acts.scenes'
                }
            },

            {
                '$group': {
                    '_id': '$_id',
                    'act': {
                        '$first': '$acts.title'
                    },
                    'scene': {
                        '$first': '$scene.title'
                    },
                    'actions': {
                        '$count': {}
                    }
                }
            },

            {
                '$sort': {
                    'actions': -1
                }
            },

            {
                '$limit': 1
            },

            {
                '$set': {
                    'play': '$_id'
                }
            },
            {
                '$unset': '_id'
            }
        ]
    )
    pprint.pprint(list(result))


def available_commands():
    Command = namedtuple('Command', 'action, description')

    commands = dict()
    commands['0'] = Command(action=None, description='Exit program')
    commands['1'] = Command(action=find_most_actioned_play, description='Find most actioned scene among plays')
    commands['2'] = Command(action=find_most_popular_characters, description='Find most popular characters in plays')

    return commands


def print_commands(commands):
    print()
    print('Program provides such options as:')
    for key, command in commands.items():
        print('\t{} = {}'.format(key, command.description))


def main():
    commands = available_commands()

    while True:
        print_commands(commands)

        try:
            key = input('Enter option: ').strip()
        except EOFError as exc:
            key = ''

        if key == '0':
            break

        if key in commands:
            commands[key].action()
        else:
            print('Please choose proper option.')


if __name__ == '__main__':
    main()
