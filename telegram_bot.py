import telebot
import pymongo
import logging
from settings import config
bot = telebot.TeleBot(config.telegram_key)
client = pymongo.MongoClient(config.mongodb_key)
db_name = "Event"
collection_name = "Questions"
db = client[db_name][collection_name]
dic_user = {}
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
@bot.message_handler(commands=['start'])
def _start(message):
    msg = "Hello "+str(message.chat.username)+\
          ", I'm a date reminder. Tell me birthdays and events to remind you. To learn how to use me, use \n/help"
    bot.send_message(message.chat.id, msg)
@bot.message_handler(commands=['hello'])
def _start(message):
    msg = "Hello"
    bot.send_message(message.chat.id, msg)
if config.ENV == "DEV":
    bot.infinity_polling(True)  #bot.polling()


elif config.ENV == "PROD":
    import flask
    import threading

    server = flask.Flask(__name__)

    @server.route('/'+config.telegram_key, methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url='https://beat-the-bot.herokuapp.com/'+config.telegram_key)
        return 'Chat with the Bot  <a href ="https://t.me/DatesReminderBot">here</a> \
          or   Check the project code <a href ="https://github.com/mdipietro09/Bot_TelegramDatesReminder">here</a>', 200

    if __name__ == "__main__":
        server.run(host=config.host, port=config.port)
