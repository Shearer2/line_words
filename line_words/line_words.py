import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os


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
        self.password ='alegedor0012'  # input('Введите ваш пароль: '),
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


# Загружаем переменные среды, которые нужно скрыть от постронних глаз.
load_dotenv()
# Необходимо инициализировать объекты bot и Dispatcher, передав первому токен. Если этого не сделать, то код не будет
# работать. Забираем значение нашего токена.
bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)
HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>начать работу с ботом</em>
<b>/links</b> - <em>перейти в репозиторий github</em>
<b>/projects</b> - <em>ознакомиться с проектами</em>
<b>/description</b> - <em>описание проекта</em>
<b>/vote</b> - <em>голосование</em>
"""


# Отображение информации в консоли, что бот работает.
async def on_startup(_):
    print("Бот включён.")


# Чтобы настроить приветственное окно для нового пользователя, которое будет появляться при нажатии команды /start,
# необходимо создать message_handler и прописать функцию ответа.
@dp.message_handler(commands='start')  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    # Для асинхронной работы бота пишем await. Бот отвечает на сообщение при помощи reply.
    # parse_mode позволяет указывать какой-то язык, чтобы в тексте использовать функционал данного языка.
    await message.reply("<em>Привет! 🤚\n Я - бот 🤖, предназначенный для игры линия слова.</em>", parse_mode="HTML")
    # Для отправки сообщения туда, где пишет пользователь, нужно указывать message.chat.id. Для отправки сообщения
    # только в личные сообщения пользователю, даже если он пишет в группе, используется message.from_user.id.
    await bot.send_photo(chat_id=message.chat.id, photo="https://play-lh.googleusercontent.com/F3mmWSAnQ8Y3ys8KY8v0tD0Sd1hLHoSbA3SGsmQWbt5KsZq9rh2grAefGbgQKkv2Tlg")


# В качестве команды вызова указываем ссылки, а в параметре reply_markup передаём название нашей клавиатуры.
@dp.message_handler(commands='links')
async def url_command(message: types.Message):
    # Пишем сообщение пользователю при помощи answer.
    #await message.answer('Полезные ссылки:', reply_markup=urlkb)
    pass


@dp.message_handler(commands='help')
async def bot_help(message: types.Message):
    await message.answer(HELP_COMMAND, parse_mode="HTML")
    #await message.answer('Бот создан для отгадывания слов из букв в игре Линия слова.\n'
    #                     'Введите буквы и получите все возможные слова.')


@dp.message_handler(commands='projects')
async def projects(message: types.Message):
    await message.answer('Мои проекты:', reply_markup=urlkb)


# Функция для отправки стикеров.
@dp.message_handler(commands='give')
async def bot_sticker(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker="CAACAgIAAxkBAAEKCmFk3KOnuqxhgaM2DFhFG3VyNWsHtQACPwADQdL3IfZZVXp87Hm5MAQ")
    await message.answer('Люблю Миланочку чудесную')


@dp.message_handler(content_types='sticker')
async def send_sticker_id(message: types.Message):
    await message.reply(f"Id стикера:\n{message.sticker.file_id}")


@dp.message_handler(commands='description')
async def bot_description(message: types.Message):
    await message.answer("Описание проекта.")


@dp.message_handler(commands='vote')
async def bot_vote(message: types.Message):
    ikb = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="Да", callback_data="like")
    button2 = InlineKeyboardButton(text="Нет", callback_data="dislike")
    ikb.add(button1, button2)
    await message.answer("Все ли слова угадываются?", reply_markup=ikb)


# Создаём callback функцию для голосования.
@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        # Не нужно указывать return, так как callback.answer завершает исполнение callback функции.
        await callback.answer('Слов хватает')
    await callback.answer('Слов не хватает')


# Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
@dp.message_handler()
async def echo(message: types.Message):
    kb = [
        [
            # Создаём кнопки.
            KeyboardButton(text="/help"),
            KeyboardButton(text="/links"),
            KeyboardButton(text="/projects")
        ],
        [
            KeyboardButton(text="/description"),
            KeyboardButton(text="/vote")
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
urlButton = InlineKeyboardButton(text='Линия слова', url='https://github.com/Shearer2/line_words')
urlButton2 = InlineKeyboardButton(text='Угадывание чисел', url='https://github.com/Shearer2/Random_numbers')
urlButton3 = InlineKeyboardButton(text='Угадывание слов', url='https://github.com/Shearer2/Random_word')
urlButton4 = InlineKeyboardButton(text='Парсер телеграм каналов', url='https://github.com/Shearer2/Parser_telegram')
urlButton5 = InlineKeyboardButton(text='Адаптивный сайт', url='https://github.com/Shearer2/Adaptive-site')
# Добавляем кнопки к уже созданной клавиатуре.
urlkb.add(urlButton, urlButton2, urlButton3, urlButton4, urlButton5)


# Настраиваем получение сообщений от сервера в телеграм. Если этого не сделать, то мы не получим ответы бота.
# start_polling опрашивает сервер, проверяя на нём обновления, если они есть, то они приходят в телеграм.
if __name__ == '__main__':
    # skip_updates нужно чтобы все обновления пропускались. Если будет False, то при каждом запуске бот будет пытаться
    # ответить на все сообщения, которые были отправлены, пока он был выключен.
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
