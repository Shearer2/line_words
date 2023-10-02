import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


class WordLine:
    def __init__(self, letters):
        self.letters = letters

    # Функция для получения всех слов из базы данных.
    @staticmethod
    def search_database():
        # Подключаемся к базе данных.
        connection = psycopg2.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('db_name')
        )
        # Нужно для отработки запроса и записи изменений в базу данных.
        connection.autocommit = True

        # Получаем все слова из базы данных.
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT word FROM words.all_words"""
            )
            # Собираем все записи в список.
            words = list(map(lambda x: x[0], cursor.fetchall()))

        return words

    # Функция для вывода только тех слов, которые подходят.
    def right_words(self):
        result_start = 'Возможные слова:\n'
        result = []
        flag = False
        words = self.search_database()
        # Берём каждое слово из базы данных.
        for word in words:
            # Если отсортированное слово совпадает с отсортированными буквами, которые ввёл пользователь, то добавляем
            # его в список для вывода.
            if sorted(word) == sorted(self.letters):
                result.append(word)
            # Иначе проверяем каждую букву в слове.
            else:
                for i in word:
                    # Если количество определённых букв в слове совпадает с количеством этих же букв среди
                    # пользовательских букв, то ставим флаг True, иначе False.
                    if word.count(i) == self.letters.count(i):
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
