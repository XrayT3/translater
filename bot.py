import xml.dom.minidom
import telebot
import urllib
import time
from Translater import config

key = 'trnsl.1.1.20170503T205407Z.df3292ae8a21d767.fc3f096cd744f300221740b9ed1d82ff0e05402a'
token = '399866330:AAELIR8PEF3N5skoB6kpU3-IVosVLM3VY1w'
lang = 'ru'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'lang'])
def change_language(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Выбрать язык')
    bot.send_message(message.chat.id, "Привет, выбери язык, на который нужно перевести.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'en')
def language(call):
    global lang
    lang = 'en'
    print(lang)


@bot.callback_query_handler(func=lambda call: call.data == 'ru')
def language(call):
    global lang
    lang = 'ru'
    print(lang)


@bot.callback_query_handler(func=lambda call: call.data == 'es')
def language(call):
    global lang
    lang = 'es'
    print(lang)


@bot.callback_query_handler(func=lambda call: call.data == 'de')
def language(call):
    global lang
    lang = 'de'
    print(lang)


@bot.callback_query_handler(func=lambda call: call.data == 'fr')
def language(call):
    global lang
    lang = 'fr'
    print(lang)


@bot.callback_query_handler(func=lambda call: call.data == 'cs')
def language(call):
    global lang
    lang = 'cs'
    print(lang)


@bot.message_handler(regexp='Выбрать язык')
def client_panel(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_en = telebot.types.InlineKeyboardButton(text="Английский", callback_data='en')
    btn_ru = telebot.types.InlineKeyboardButton(text="Русский", callback_data='ru')
    btn_es = telebot.types.InlineKeyboardButton(text="Испанский", callback_data='es')
    btn_de = telebot.types.InlineKeyboardButton(text="Немецкий", callback_data='de')
    btn_fr = telebot.types.InlineKeyboardButton(text="Французкий", callback_data='fr')
    btn_cs = telebot.types.InlineKeyboardButton(text="Чешский", callback_data='cs')
    markup.add(btn_en, btn_ru)
    markup.add(btn_es, btn_de)
    markup.add(btn_fr, btn_cs)
    bot.send_message(message.chat.id, "Языки", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def translate(message):
    text = message.text
    print(lang)
    args = {'key': key, 'text': text, 'lang': lang}
    enc_args = urllib.parse.urlencode(args)
    response = urllib.request.urlopen('https://translate.yandex.net/api/v1.5/tr/translate?' + enc_args)
    xml_file = response.read()
    xml_file = xml_file.decode('utf-8')
    dom = xml.dom.minidom.parseString(xml_file)
    dom.normalize()
    text = dom.getElementsByTagName("text")[0]
    bot.send_message(message.chat.id, text.childNodes[0].nodeValue)
    return text


# Запуск бота

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as expt:
        config.log(Exception='HTTP_CONNECTION_ERROR', text=expt)
        print('Connection lost..')
        time.sleep(30)
        continue
    except r_exceptions.Timeout as exptn:
        config.log(Exception='HTTP_REQUEST_TIMEOUT_ERROR', text=exptn)
        time.sleep(5)
        continue