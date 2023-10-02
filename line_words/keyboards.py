from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Создание клавиатуры для любого текста.
def get_kb() -> ReplyKeyboardMarkup:
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

    return keyboard


# Создание клавиатуры для проектов.
def get_url_kb() -> InlineKeyboardMarkup:
    # Аргумент row_width определяет сколько кнопок будет находиться в одном ряду.
    url_kb = InlineKeyboardMarkup(row_width=1)
    # Создаём кнопки с указанием текста и ссылки, по которой будет осуществляться переход при нажатии.
    url_btn1 = InlineKeyboardButton(text='Линия слова', url='https://t.me/s/Line_words_bot/')
    url_btn2 = InlineKeyboardButton(text='Заметки', url='https://t.me/s/saved_notes_bot/')
    url_btn3 = InlineKeyboardButton(text='Висельница', url='https://t.me/s/Game_Gallow_Bot/')
    # Добавляем кнопки к уже созданной клавиатуре.
    url_kb.add(url_btn1, url_btn2, url_btn3)
    return url_kb


# Создание клавиатуры для голосования.
def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="Да", callback_data="like")
    button2 = InlineKeyboardButton(text="Нет", callback_data="dislike")
    ikb.add(button1, button2)
    return ikb


def get_github() -> InlineKeyboardMarkup:
    url_kb = InlineKeyboardMarkup(row_width=1)
    url_btn = InlineKeyboardButton(text='Github', url='https://github.com/Shearer2?tab=repositories')
    url_kb.add(url_btn)

    return url_kb
