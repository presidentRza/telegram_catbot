#! /usr/bin/python2
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, \
    ReplyKeyboardMarkup, KeyboardButton

import requests
import sys

try:
    from secret_chat_keyqqwd import TOKEN
except ImportError as e:  # Exception as e:
    print(type(e))
    import os  # fallback on Heroku server
    try:
        TOKEN = os.environ['TOKEN']
    except KeyError:
        print("'TOKEN' not in ENV")
    print("Read token from env: " + str(TOKEN))

def get_random_cat_url():
    response = requests.get(url="https://api.thecatapi.com/v1/images/search")
    cat_url = str(response.json()[0]['url'])
    return cat_url


class DemoTelegramBot:
    def __init__(self):
        self.with_webhooks = False
        self.updater = Updater(token=TOKEN)

        if self.with_webhooks:
            self.updater.start_webhook(listen='127.0.0.1', port=8443, url_path=TOKEN)
            self.updater.bot.set_webhook(webhook_url='https://my_server.com/' + TOKEN,
                                         certificate=open('webhook_cert.pem', 'rb'))

        self.dispatcher = self.updater.dispatcher

        # create callbacks for '/help' and '/options'
        self.dispatcher.add_handler(CommandHandler("help", self.on_help))
        self.dispatcher.add_handler(CommandHandler("options", self.on_options))
        self.dispatcher.add_handler(CommandHandler("location", self.on_location))
        self.dispatcher.add_handler(CommandHandler("cat", self.on_cat))

        # Callback for normal messages from user
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.text_cb))

        # Callback for position
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.got_location))

        # callback for custom keyboards
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.mode_button_cb))

    @staticmethod
    def on_options(bot, update):
        # encode question is callback_data ('w'): hack, could be something better
        keyboard = [[InlineKeyboardButton("Bad", callback_data='w,1'),
                     InlineKeyboardButton("OK", callback_data='w,2'),
                     InlineKeyboardButton("Great", callback_data='w,3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('How is the weather today?', reply_markup=reply_markup)

    @staticmethod
    def mode_button_cb(bot, update):
        assert isinstance(update, Update)
        assert isinstance(update.callback_query, CallbackQuery)
        # user_id = update.callback_query.from_user.id

        query = update.callback_query

        ans = query.data.split(',')
        cmd = str(ans[0])
        value = int(ans[1])

        if cmd == 'w':
            text = "Weather score of %i" % value
        else:
            text = "Unhandled callback_data %s" % query.data
            print(text)

        # Replace keyboard with this message
        bot.edit_message_text(text=text, chat_id=query.message.chat_id, message_id=query.message.message_id)

    @staticmethod
    def text_cb(bot, update):
        assert isinstance(update, Update)
        # print (update) -> https://www.cleancss.com/python-beautify/
        first_name = update.message.chat.first_name
        msg = "Hello %s: %s (you can also use /help)" % (first_name, update.message.text.upper())
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        bot.send_photo(chat_id=update.message.chat_id, photo=get_random_cat_url())

    @staticmethod
    def got_location(bot, update):
        assert isinstance(update, Update)
        a, b = update.message.location.latitude, update.message.location.longitude
        bot.send_message(chat_id=update.message.chat_id, text="You are at %.3f, %.3f" % (a, b))

    @staticmethod
    def on_location(bot, update):
        location_keyboard = [[KeyboardButton(text="Send my location", request_location=True)]]
        update.message.reply_text('Please share your location.',
                                  reply_markup=ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True))

    @staticmethod
    def on_help(bot, update):
        update.message.reply_text(u'Send any message to get an uppercase response. \n'
                                  u'/location to send your location \n️'
                                  u'/cat to get a cat image \n️'
                                  u'/options to talk about weather️ ☺')

    @staticmethod
    def on_cat(bot, update):
        bot.send_photo(chat_id=update.message.chat_id, photo=get_random_cat_url())

    def run(self):
        if not self.with_webhooks:
            print("start polling")
            sys.stdout.flush()
            self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    dtb = DemoTelegramBot()
    dtb.run()
