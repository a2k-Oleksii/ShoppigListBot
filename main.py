
import telebot
import flask
import time

API_TOKEN = "6454697652:AAEBf2IBBK4NUsJ0jqtyHW4tyHMPthGZvhY"
shop_bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)

WEBHOOK_HOST = "2f4a-178-214-192-176.ngrok-free.app"
WEBHOOK_PORT = 8448
WEBHOOK_LISTEN = "0.0.0.0"

WEBHOOK_URL_BASE = "https://%s" % WEBHOOK_HOST
WEBHOOK_URL_PATH = "/%s/" % API_TOKEN

commands = ["Add to list", "Get from list", "Delete from list"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*commands)

user_data = {}


@app.route("/", methods=["GET", "HEAD"])
def index():
    print("index")
    return "Shopping Bot"


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        shop_bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


@shop_bot.message_handler(commands=["start"])
def start(message):
    shop_bot.reply_to(message, "Welcome to shopping bot!", reply_markup=keyboard)


@shop_bot.message_handler(content_types=["text"])
def command(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = [[], None, None]
    if message.text == "Add to list":
        user_data[message.chat.id][1] = "add"
        shop_bot.reply_to(message, "You can add items to the list")
    elif message.text == "Get from list":
        user_data[message.chat.id][1] = "get"
        shop_bot.reply_to(message, ", ".join(user_data[message.chat.id][0]) if user_data[message.chat.id][0] else "Your shopping list is empty")
    elif message.text == "Delete from list":
        user_data[message.chat.id][1] = "del"
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row_width = 2
        for elem in user_data[message.chat.id][0]:
            inline_keyboard.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
        res = shop_bot.reply_to(message, "Delete items", reply_markup=inline_keyboard)
        user_data[message.chat.id][2] = res.message_id
    else:
        if user_data[message.chat.id][1] == "add":
            user_data[message.chat.id][0].append(message.text)
            shop_bot.reply_to(message, f"Successfully added {message.text}")


@shop_bot.callback_query_handler(func=lambda x: True)
def callback_handler(call):
    for i in range(len(user_data[call.message.chat.id][0])):
        if user_data[call.message.chat.id][0][i] == call.data:
            del user_data[call.message.chat.id][0][i]
            break
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    inline_keyboard.row_width = 2
    for elem in user_data[call.message.chat.id][0]:
        inline_keyboard.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
    shop_bot.edit_message_reply_markup(call.message.chat.id, user_data[call.message.chat.id][2], reply_markup=inline_keyboard)


shop_bot.remove_webhook()
time.sleep(0.1)

shop_bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app.run(host="localhost", port=8448)
