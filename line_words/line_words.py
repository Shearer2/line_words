import psycopg2
import requests
from bs4 import BeautifulSoup as BS


def all_words():
    letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    result = []
    for i in letters:
        r = requests.get(f'https://kupidonia.ru/spisok/spisok-suschestvitelnyh-russkogo-jazyka/bukva/{i}')
        html = BS(r.content, 'html.parser')
        word = html.findAll('div', class_='position_title')
        result.extend(''.join([w.text for w in word]).split())
    return result


def add_database(all_words):
    connection = psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        password=input('Введите ваш пароль: '),
        database='line_words'
    )
    connection.autocommit = True
    for i in range(len(all_words)):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO words.all_words (word) VALUES ('{all_words[i]}')"""
            )
    connection.close()


all_words = all_words()
