import psycopg2
import requests
from bs4 import BeautifulSoup as BS
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Bot - определяет, на какие команды от пользователя и каким способом отвечать.
# Dispatcher - позволяет отслеживать обновления.
# Executor - запускает бота и выполняет функции, которые следует выполнить.
# Types - позволяет использовать базовые классы для аннотирования, то есть восприятия сообщений.
# ReplyKeyboardRemove и ReplyKeyboardMarkup позволяют создавать и удалять клавиатуру, а класс KeyboardButton
# используется для добавления кнопок.
# Reply-кнопки прикрепляются к клавиатуре, а инлайн-кнопки прикрепляются к сообщению.
# InlineKeyboardMarkup пригодится для инициализации инлайн-кнопок, а InlineKeyboardButton - для их создания.
class WordLine:
    def __init__(self, letters):
        self.host = '127.0.0.1'
        self.user = 'postgres'
        self.password = input('Введите ваш пароль: '),
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
        result.sort(key=len)
        result.reverse()
        if len(result) > 1:
            return '\n'.join(result)
        return 'Слов с такими буквами нет.'


API_TOKEN = '6398703102:AAH-c3FCv37FTnF0hDXdz1pS3fTMRnBjGDc'
# Необходимо инициализировать объекты bot и Dispatcher, передав первому токен. Если этого не сделать, то код не будет
# работать.
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
HELP_COMMAND = """
/help - список команд
/start - начать работу с ботом
/links - перейти в репозиторий github
/projects - ознакомиться с проектами
"""


# Чтобы настроить приветственное окно для нового пользователя, которое будет появляться при нажатии команды /start,
# необходимо создать message_handler и прописать функцию ответа.
@dp.message_handler(commands='start')  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    # Для асинхронной работы бота пишем await. Бот отвечает на сообщение при помощи reply.
    await message.reply("Привет!\n Я - бот, предназначенный для игры линия слова.")


# В качестве команды вызова указываем ссылки, а в параметре reply_markup передаём название нашей клавиатуры.
@dp.message_handler(commands='links')
async def url_command(message: types.Message):
    # Пишем сообщение пользователю при помощи answer.
    await message.answer('Полезные ссылки:', reply_markup=urlkb)


@dp.message_handler(commands='help')
async def bot_help(message: types.Message):
    await message.answer(HELP_COMMAND)
    #await message.answer('Бот создан для отгадывания слов из букв в игре Линия слова.\n'
    #                     'Введите буквы и получите все возможные слова.')


@dp.message_handler(commands='projects')
async def projects(message: types.Message):
    pass


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
# Создаём функцию с простой задачей - отправить обратно тот же текст, что ввёл пользователь.
async def echo(message: types.Message):
    kb = [
        [
            # Создаём кнопки.
            KeyboardButton(text="/help"),
            KeyboardButton(text="/links"),
            KeyboardButton(text="/projects")
        ],
    ]
    # Создаём клавиатуру и рассказываем ей про наши кнопки.
    # Чтобы автоматически уменьшить размер кнопок указываем resize_keyboard=True.
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    # В строку для ответа добавляем reply_markup=keyboard, чтобы показать клавиатуру в телеграм.
    word_line = WordLine(message.text.lower())
    await message.answer(text=word_line.search_database(), reply_markup=keyboard)


# Аргумент row_width определяет сколько кнопок будет находиться в одном ряду.
urlkb = InlineKeyboardMarkup(row_width=1)
# Создаём кнопки с указанием текста и ссылки, по которой будет осуществляться переход при нажатии.
urlButton = InlineKeyboardButton(text='Перейти в github', url='https://github.com/Shearer2?tab=repositories')
#urlButton2 = InlineKeyboardButton(text='Перейти к курсам', url='https://skillbox.ru/code/')
# Добавляем две кнопки к уже созданной клавиатуре.
#urlkb.add(urlButton, urlButton2)
urlkb.add(urlButton)


# Настраиваем получение сообщений от сервера в телеграм. Если этого не сделать, то мы не получим ответы бота.
# start_polling опрашивает сервер, проверяя на нём обновления, если они есть, то они приходят в телеграм.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
