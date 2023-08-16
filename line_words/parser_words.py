import psycopg2
import requests
from bs4 import BeautifulSoup as BS


def all_words() -> list:
    letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    result = []
    for i in letters:
        r = requests.get(f'https://kupidonia.ru/spisok/spisok-suschestvitelnyh-russkogo-jazyka/bukva/{i}')
        html = BS(r.content, 'html.parser')
        word = html.findAll('div', class_='position_title')
        result.extend(''.join([w.text for w in word]).split())
    return result


def nouns_singular(nouns: list):
    result = []
    for noun in nouns:
        #if len(noun) > 2 and '-' not in noun and not noun.endswith('ые') and not noun.endswith('ы'):
        #    result.append(noun)
        if len(noun) > 2 and '-' not in noun:
            result.append(noun)
    return result


def add_database(words: list):
    connection = psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        password=input('Введите ваш пароль: '),
        database='line_words'
    )
    connection.autocommit = True
    for i in range(len(words)):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO words.all_words (word) VALUES ('{words[i]}')"""
            )
    connection.close()


with open('russian_nouns.txt', 'r', encoding='utf-8') as words_all:
    mapped = list(map(lambda x: x.split()[0], words_all.readlines()))

#mapped.extend(all_words())
#nouns = sorted(set(mapped))
#parser = nouns_singular(nouns)
#add_database(parser)
parser = nouns_singular(mapped)
add_database(parser)
