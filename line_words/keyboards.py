from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Создание клавиатуры для любого текста.
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

# Создание клавиатуры для проектов.
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

# Создание клавиатуры для голосования.
ikb = InlineKeyboardMarkup(row_width=1)
button1 = InlineKeyboardButton(text="Да", callback_data="like")
button2 = InlineKeyboardButton(text="Нет", callback_data="dislike")
ikb.add(button1, button2)
