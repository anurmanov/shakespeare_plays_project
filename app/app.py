import os
import sys
import traceback
import pprint
from functools import wraps
from collections import namedtuple
import pymongo


def mongo_connection(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        client = None
        try:
            uri = 'mongodb://{}:{}@{}:{}/?authSource=admin'.format(
                os.getenv('DB_USER'),
                os.getenv('DB_PASSWORD'),
                os.getenv('MONGO_HOST'),
                os.getenv('MONGO_EXTERNAL_PORT'),
            )
            client = pymongo.MongoClient(uri
                                         )
            result = f(client, *args, **kwargs)
         
        except Exception as exc:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            raise RuntimeError('Error occurred. Details: {}'.format(trace)) from exc
        
        finally:
            if client:
                client.close()

        return result

    return wrapper


@mongo_connection
def find_most_popular_characters(client):
    """
    Поиск самых популярных имен персонажей во всех пьесах
    """

    db = client[os.getenv('DB_NAME')]
    plays = db.plays

    result = plays.aggregate(
        [
            #распаковка массива актов - аналог обхода через цикл for
            {
                '$unwind': {
                    'path': '$acts',
                    'preserveNullAndEmptyArrays': True
                }
            },
            #распаковка массива сцен
            {
                '$unwind': {
                    'path': '$acts.scenes',
                    'preserveNullAndEmptyArrays': True
                }
            },
            #распаковка массива реплик
            {
                '$unwind': {
                    'path': '$acts.scenes.action',
                    'preserveNullAndEmptyArrays': True
                }
            },
            #установка атрибутов play и character
            {
                '$set': {
                    'play': '$_id',
                    'character': {"$toUpper": "$acts.scenes.action.character"}
                }
            },
            #удаление полей acts, _id
            {
                '$unset': [
                    'acts', '_id'
                ]
            },
            #групировка по персонажу с добавлением пьес во множество
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
            #установка атрибута acted_in_plays - количество сыгранных пьес
            {
                '$set': {
                    'acted_in_plays': {
                        '$size': '$plays'
                    }
                }
            },
            #удаление атрибута _id
            {
                '$unset': '_id'
            },
            #отбираем все документы, у которых персонаж сыграл в пьесе больше 1 раза
            {
                '$match': {
                    'acted_in_plays': {
                        '$gt': 1
                    }
                }
            },
            #сортируем по убыванию acted_in_plays - количество сыгранных пьес
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
    """
    Поиск пьесы с наибольшим количеством реплик (actions) в пьесах
    """

    db = client[os.getenv('DB_NAME')]
    plays = db.plays

    result = plays.aggregate(
        [
            #распаковка актов пьес
            {
                '$unwind': {
                    'path': '$acts',
                    'preserveNullAndEmptyArrays': True
                }
            },
            # распаковка сцен актов
            {
                '$unwind': {
                    'path': '$acts.scenes'
                }
            },
            #установка поля scene для удобства
            {
                '$set': {
                    'scene': '$acts.scenes'
                }
            },
            #группировка документов по пьесе, акту, сцене с суммированеим кол-ва актов
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
            #сортируем по убыванию количества актов
            {
                '$sort': {
                    'actions': -1
                }
            },
            #берем 1-ый документ, соответствено с большим кол-вом актов
            {
                '$limit': 1
            },
            #установка атрибута play вместо _id
            {
                '$set': {
                    'play': '$_id'
                }
            },
            #удаление поля _id
            {
                '$unset': '_id'
            }
        ]
    )
    pprint.pprint(list(result))


def available_commands():
    Command = namedtuple('Command', 'action, description')

    commands = dict()
    commands['0'] = Command(
        action=None, 
        description='Выход из программы'
    )
    commands['1'] = Command(
        action=find_most_actioned_play, 
        description='Поиск пьесы с наибольшим количеством реплик (actions) в пьесах'
    )
    commands['2'] = Command(
        action=find_most_popular_characters, 
        description='Поиск самых популярных имен персонажей во всех пьесах'
    )

    return commands


def print_commands(commands):
    print()
    print('Программа предоставляет следующие опции:')
    for key, command in commands.items():
        print('\t{} = {}'.format(key, command.description))


def main():
    commands = available_commands()

    while True:
        print_commands(commands)

        try:
            key = input('Введите опцию: ').strip()
        except EOFError as exc:
            key = ''

        if key == '0':
            break

        if key in commands:
            commands[key].action()
        else:
            print('Пожалуйста, выберите доступную опцию от 0 до 2')


if __name__ == '__main__':
    main()
