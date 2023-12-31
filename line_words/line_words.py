import psycopg2
import os
import hashlib
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent  # Для работы инлайн режима.
from aiogram.utils.callback_data import CallbackData
from postgresql import db_start, information_id, information_vote, create_profile, delete_profile, right_words
from keyboards import get_kb, get_url_kb, get_ikb, get_github


# Bot - определяет, на какие команды от пользователя и каким способом отвечать.
# Dispatcher - позволяет отслеживать обновления.
# Executor - запускает бота и выполняет функции, которые следует выполнить.
# Types - позволяет использовать базовые классы для аннотирования, то есть восприятия сообщений.
# Загружаем переменные среды, которые нужно скрыть от постронних глаз.
load_dotenv()
# Необходимо инициализировать объекты bot и Dispatcher, передав первому токен. Если этого не сделать, то код не будет
# работать. Забираем значение нашего токена.
bot = Bot(token=os.getenv('API_TOKEN'))
# storage - это хранилище, в котором будут храниться состояния и файлы, которые отправляются боту.
dp = Dispatcher(bot=bot)
HELP_COMMAND = """
<b>/start</b> - <em>начать работу с ботом.</em>
<b>/vote</b> - <em>голосование.</em>
<b>/link</b> - <em>перейти в репозиторий github.</em>
<b>/projects</b> - <em>ознакомиться с проектами.</em>
<b>/description</b> - <em>описание проекта.</em>
<b>/help</b> - <em>вывести список команд.</em>
"""
cb = CallbackData('ikb', 'action')


# Функция для голосования.
def vote_answer():
    like = information_vote().count('like')
    dislike = information_vote().count('dislike')
    # Если лайков больше, то выводим следующее сообщение.
    if like >= dislike:
        text = f"Все ли слова угадываются?\n\n" \
               f"Слов хватает:\n" \
               f"{like * '👍'}\n" \
               f"Слов не хватает:\n" \
               f"{dislike * '👎'}"
        return text
    # Иначе выводим данный текст.
    else:
        text = f"Все ли слова угадываются?\n\n" \
               f"Слов не хватает:\n" \
               f"{dislike * '👎'}\n" \
               f"Слов хватает:\n" \
               f"{like * '👍'}"
        return text


# Отображение информации в консоли, что бот работает.
async def on_startup(_) -> None:
    await db_start()


# Чтобы настроить приветственное окно для нового пользователя, которое будет появляться при нажатии команды /start,
# необходимо создать message_handler и прописать функцию ответа.
@dp.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message) -> None:
    # Для асинхронной работы бота пишем await. Бот отвечает на сообщение при помощи reply.
    # parse_mode позволяет указывать какой-то язык, чтобы в тексте использовать функционал данного языка.
    await message.reply("<em>Привет! 🤚\n Я - бот 🤖, предназначенный для игры линия слова.</em>", parse_mode="HTML")
    # Для отправки сообщения туда, где пишет пользователь, нужно указывать message.chat.id. Для отправки сообщения
    # только в личные сообщения пользователю, даже если он пишет в группе, используется message.from_user.id.
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://play-lh.googleusercontent.com"
                               "/F3mmWSAnQ8Y3ys8KY8v0tD0Sd1hLHoSbA3SGsmQWbt5KsZq9rh2grAefGbgQKkv2Tlg")


# В качестве команды вызова указываем ссылки, а в параметре reply_markup передаём название нашей клавиатуры.
@dp.message_handler(commands=['link'])
async def bot_link(message: types.Message) -> None:
    # Пишем сообщение пользователю при помощи answer.
    await message.answer('Репозиторий github:', reply_markup=get_github())


# Делаем обработку команды help.
@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message) -> None:
    await message.answer(HELP_COMMAND, parse_mode="HTML")


# Выводим список доступных проектов.
@dp.message_handler(commands=['projects'])
async def bot_projects(message: types.Message) -> None:
    await message.answer('Мои проекты:', reply_markup=get_url_kb())


# Выводим описание бота.
@dp.message_handler(commands=['description'])
async def bot_description(message: types.Message) -> None:
    await message.answer("Данный бот выдаёт все возможные слова на введённые буквы. Есть возможность проголосовать за "
                         "то, все ли слова были найдены или нет. Можно ознакомиться с проектами автора или же с "
                         "функционалом бота через команду help.")


# Функция для проведения голосования.
@dp.message_handler(commands=['vote'])
async def bot_vote(message: types.Message) -> None:
    await message.answer(vote_answer(), reply_markup=get_ikb())


# Создаём callback функцию для голосования.
@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery) -> None:
    user_id = callback['from']['id']
    # callback - словарь, в котором хранится вся необходимая информация о пользователе, о сообщении, о выборе ответа.
    # Если была нажата кнопка like и пользователя нет в базе данных, то заносим его в базу данных и выводим
    # исправленное сообщение с его голосом.
    if callback.data == 'like' and user_id not in information_id():
        await create_profile(user_id, callback.data)
        # Не нужно указывать return, так как callback.answer завершает исполнение callback функции.
        await callback.message.edit_text(vote_answer(), reply_markup=get_ikb())
    # Иначе если пользователя нажал dislike и его нет в базе данных, то заносим в базу данных и исправляем сообщение.
    elif callback.data == 'dislike' and user_id not in information_id():
        await create_profile(user_id, callback.data)
        await callback.message.edit_text(vote_answer(), reply_markup=get_ikb())
    # Иначе если пользователь удалил свой голос и он есть в базе данных, то удаляем его голос из базы данных.
    elif callback.data == 'delete' and user_id in information_id():
        await delete_profile(user_id)
        await callback.message.edit_text(vote_answer(), reply_markup=get_ikb())
    # Иначе если пользователь пытается удалить свой голос и его нет в базе данных, то выводим сообщение, что нет голоса.
    elif callback.data == 'delete' and user_id not in information_id():
        await callback.message.answer("Вы не проголосовали!")
    # Если пользователь есть в базе данных и пытается проголосовать, то оповещаем его об этом.
    else:
        await callback.message.answer("Вы уже проголосовали!")


@dp.inline_handler()
async def inline_words(inline_query: types.InlineQuery) -> None:
    # Получаем текст пользователя.
    text = inline_query.query
    # Формируем контент ответного сообщения.
    input_content = InputTextMessageContent(right_words(text.lower()))
    # Для отправки сообщения у него должен быть уникальный идентификатор, для его получения будем использовать
    # хэш-функцию для кодирования сообщения.
    # Полученное сообщение переводим в двоичную систему счисления, затем кодируем и переводим в 16-ую систему счисления.
    result_id = hashlib.md5(text.encode()).hexdigest()

    # Чтобы отправить текстовое сообщение используется Article. Он является наиболее часто используемым классом.
    # thumb_url нужен для подстановки картинки.
    item = InlineQueryResultArticle(
        input_message_content=input_content,
        id=result_id,
        title='Линия слова',
        description='Введите буквы',
        thumb_url='https://play-lh.googleusercontent.com'
                  '/F3mmWSAnQ8Y3ys8KY8v0tD0Sd1hLHoSbA3SGsmQWbt5KsZq9rh2grAefGbgQKkv2Tlg'
    )

    # Отвечаем на инлайн запрос. Указываем id сообщения, затем передаём список из тех элементов, которыми мы будем
    # отвечать, затем указываем то время в течении которого в телеграм api будут кешироваться данные.
    await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item],
                                  cache_time=1)


# Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
@dp.message_handler()
async def words(message: types.Message) -> None:
    # В строку для ответа добавляем reply_markup=keyboard, чтобы показать клавиатуру в телеграм.
    await message.answer(text=right_words(message.text.lower()), reply_markup=get_kb())


# Настраиваем получение сообщений от сервера в телеграм. Если этого не сделать, то мы не получим ответы бота.
# start_polling опрашивает сервер, проверяя на нём обновления, если они есть, то они приходят в телеграм.
if __name__ == '__main__':
    # skip_updates нужно чтобы все обновления пропускались. Если будет False, то при каждом запуске бот будет пытаться
    # ответить на все сообщения, которые были отправлены, пока он был выключен.
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
