import telebot
import os
from dotenv import load_dotenv
from telebot import types
from logic import pars_taobao


# загружаем переменные окружения
load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start', 'taobao'])
def start(message):
    user_id = message.chat.id
    if message.text == '/start':

        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Taobao', callback_data='taobao')
        )

        bot.send_message(user_id,
                         'Добро пожаловать!\n'
                         'выберите магазин для парсинга',
                         reply_markup=markup)

    elif message.text == '/taobao':
        bot.send_message(user_id, 'Отправьте ссылку на товар.')
        bot.register_next_step_handler(message, taobao)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    call_back = call.data
    user_id = call.message.chat.id

    if call_back == 'taobao':
        bot.send_message(user_id, 'Отправьте ссылку на товар.')
        bot.register_next_step_handler(call.message, taobao)


def taobao(message):
    user_id = message.chat.id
    try:
        url = message.text
        bot.send_message(user_id, 'Загружаю...')
        data = pars_taobao(url)
        if data['ok'] is True:
            if data['img'] is not None:
                images = []
                for n, i in enumerate(data['img']):
                    caption = None
                    if n == 0:
                        caption = data['title'] + '\n\n' + data['price']
                    images.append(types.InputMediaPhoto(i, caption=caption))

                chunk_size = 10
                chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]
                for chunk in chunks:
                    bot.send_media_group(user_id, chunk)
            else:
                bot.send_message(user_id, data['title'] + '\n\n' + data['price'])
            if 'videos' in data:
                videos = []
                for video in data['videos'][:4]:
                    videos.append(types.InputMediaVideo(video))
                bot.send_media_group(user_id, videos)
            if data['description'] is not None:
                file = open('Описание.txt', 'w', encoding='utf-8')
                file.write(data['description'])
                file.close()
                bot.send_document(user_id, open('Описание.txt', 'r', encoding='utf-8'))
        else:
            bot.send_message(user_id, 'Неверная ссылка.')
    except IndexError:
        bot.send_message(user_id, 'Неверная ссылка.')


bot.infinity_polling()
