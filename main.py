import telebot
import os
from dotenv import load_dotenv
from telebot import types
import logic


# загружаем переменные окружения
load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start', 'taobao', 'yangkeduo'])
def start(message):
    user_id = message.chat.id
    if message.text == '/start':

        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Taobao', callback_data='taobao')
        ).add(
            types.InlineKeyboardButton('Yangkeduo', callback_data='yangkeduo')
        )

        bot.send_message(user_id,
                         'Добро пожаловать!\n'
                         'выберите магазин для парсинга',
                         reply_markup=markup)

    elif message.text == '/taobao':
        bot.send_message(user_id, 'Отправьте ссылку на товар.')
        bot.register_next_step_handler(message, taobao)

    elif message.text == '/yangkeduo':
        bot.send_message(user_id, 'Отправьте ссылку на товар.')
        bot.register_next_step_handler(message, yangkeduo)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    call_back = call.data
    user_id = call.message.chat.id

    if call_back == 'taobao':
        bot.send_message(user_id, 'Отправьте ссылку на товар.')
        bot.register_next_step_handler(call.message, taobao)

    if call_back == 'yangkeduo':
        bot.send_message(user_id, 'Отправьте ссылку на товар.')
        bot.register_next_step_handler(call.message, yangkeduo)


def yangkeduo(message):
    user_id = message.chat.id
    url = message.text
    bot.send_message(user_id, 'Загружаю...')
    data = logic.pars_yangkeduo(url)
    if data['ok'] is True:
        text = f'{data['price']}\n\n{data['description']}'[:1024]
        if data['img'] is not None:
            images = []
            for n, i in enumerate(data['img']):
                caption = None
                if n == 0:
                    caption = text
                images.append(types.InputMediaPhoto(i, caption=caption))

            chunk_size = 10
            chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]
            for chunk in chunks[::-1]:
                bot.send_media_group(user_id, chunk)
        else:
            bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, 'Неверная ссылка.')


def taobao(message):
    user_id = message.chat.id
    try:
        url = message.text
        bot.send_message(user_id, 'Загружаю...')
        data = logic.pars_taobao(url)
        if data['ok'] is True:
            text = f'{data['title']}\n\n{data['price']}\n\n{data['specifications']}'
            text_singly = False
            if len(text) > 1023:
                text_singly = True
            if data['img'] is not None:
                images = []
                for n, i in enumerate(data['img']):
                    caption = None
                    if n == 0:
                        if not text_singly:
                            caption = text
                        else:
                            caption = None
                    images.append(types.InputMediaPhoto(i, caption=caption))

                chunk_size = 10
                chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]
                for chunk in chunks[::-1]:
                    bot.send_media_group(user_id, chunk)
                if text_singly:
                    chunk_size = 4094
                    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
                    for chunk in chunks:
                        bot.send_message(user_id, chunk)
            else:
                bot.send_message(user_id, text)

        else:
            bot.send_message(user_id, 'Неверная ссылка.')
    except IndexError:
        bot.send_message(user_id, 'Неверная ссылка.')


bot.infinity_polling()
