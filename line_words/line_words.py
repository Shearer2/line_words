import psycopg2
import requests
from bs4 import BeautifulSoup as BS
from aiogram import Bot, Dispatcher, executor, types


# Bot - определяет, на какие команды от пользователя и каким способом отвечать.
# Dispatcher - позволяет отслеживать обновления.
# Executor - запускает бота и выполняет функции, которые следует выполнить.
# Types - позволяет использовать базовые классы для аннотирования, то есть восприятия сообщений.
class Word_line:
    def __init__(self, letters):
        self.host = '127.0.0.1'
        self.user = 'postgres'
        self.password = 'alegedor0012'
        self.database = 'line_words'
        self.letters = letters

    def search_database(self):
        connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,  # input('Введите ваш пароль: '),
            database=self.database
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT word FROM words.all_words"""
            )
            # Собираем все записи в список.
            words = list(map(lambda x: x[0], cursor.fetchall()))

        connection.close()
        return self.right_words(words)

    def right_words(self, words: list):
        result = ['Возможные слова:']
        flag = False
        for word in words:
            if sorted(word) == sorted(self.letters):
                result.append(word)
            else:
                for i in word:
                    if word.count(i) == self.letters.count(i):
                        flag = True
                    else:
                        flag = False
                        break
                if flag:
                    result.append(word)
        return '\n'.join(result)


API_TOKEN = '6398703102:AAH-c3FCv37FTnF0hDXdz1pS3fTMRnBjGDc'
# Необходимо инициализировать объекты bot и Dispatcher, передав первому токен. Если этого не сделать, то код не будет
# работать.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Чтобы настроить приветственное окно для нового пользователя, которое будет появляться при нажатии команды /start,
# необходимо создать message_handler и прописать функцию ответа.
@dp.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    # Для асинхронной работы бота пишем await.
    await message.reply("Привет!\n Я - бот, предназначенный для игры линия слова.")


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
# Создаём функцию с простой задачей - отправить обратно тот же текст, что ввёл пользователь.
async def echo(message: types.Message):
    #await message.answer(message.text)
    word_line = Word_line(message.text)
    await message.answer(word_line.search_database())


# Настраиваем получение сообщений от сервера в телеграм. Если этого не сделать, то мы не получим ответы бота.
# start_polling опрашивает сервер, проверяя на нём обновления, если они есть, то они приходят в телеграм.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
