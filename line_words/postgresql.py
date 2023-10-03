import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

# Подключаемся к базе данных.
connection = psycopg2.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('db_name')
)
# Нужно для отработки запроса и записи изменений в базу данных.
connection.autocommit = True


# Функция для получения всех слов из базы данных.
def search_database():
    # Получаем все слова из базы данных.
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT word FROM words.all_words"""
        )
        # Собираем все записи в список.
        words = list(map(lambda x: x[0], cursor.fetchall()))

    return words


# Функция для получения id пользователей.
def information_id():
    # Получаем информацию из базы данных при помощи контекстного менеджера.
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT user_id FROM vote.people"""
        )
        inf_user = list(map(lambda x: x[0], cursor.fetchall()))
    return inf_user


# Функция для вывода только тех слов, которые подходят.
def right_words(letters):
    result_start = 'Возможные слова:\n'
    result = []
    flag = False
    words = search_database()
    # Берём каждое слово из базы данных.
    for word in words:
        # Если отсортированное слово совпадает с отсортированными буквами, которые ввёл пользователь, то добавляем
        # его в список для вывода.
        if sorted(word) == sorted(letters):
            result.append(word)
        # Иначе проверяем каждую букву в слове.
        else:
            for i in word:
                # Если количество определённых букв в слове совпадает с количеством этих же букв среди
                # пользовательских букв, то ставим флаг True, иначе False.
                if word.count(i) == letters.count(i):
                    flag = True
                else:
                    flag = False
                    break
            # Если по завершению проверки флаг будет True, то добавляем данное слово в список для вывода.
            if flag:
                result.append(word)
    # Сортируем список по длине слов.
    result.sort(key=len)
    # Разворачиваем полученный отсортированный список.
    result.reverse()
    # Если длина списка больше 1, то возвращаем список слов пользователю, иначе возвращаем текст, что слов нет.
    if len(result) > 1:
        return result_start + '\n'.join(result)
    return 'Слов с такими буквами нет.'


# Асинхронная функция для запуска базы данных.
async def db_start():
    # При помощи контекстного менеджера создаём таблицу в базе данных, если она ещё не была создана.
    with connection.cursor() as cursor:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS vote.people(user_id bigserial PRIMARY KEY, voice varchar(255))"
        )


# Создаём функцию, которая будет запускаться при команде старт и создавать запись.
async def create_profile(user_id, voice):
    # Если id пользователя нет в базе данных.
    if user_id not in information_id():
        # Создаём пустой профиль, а при команде create начнём его заполнять.
        with connection.cursor() as cursor:
            cursor.execute(f"""
                    INSERT INTO vote.people(user_id, voice) VALUES ({user_id}, '{voice}')
                """)


# Функция для удаления голоса.
async def delete_profile(user_id):
    # Если id пользователя есть в базе данных.
    if user_id in information_id():
        with connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM vote.people WHERE user_id = '{user_id}'
            """)
