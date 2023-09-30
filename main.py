import telebot

API_TOKEN = "6454697652:AAEBf2IBBK4NUsJ0jqtyHW4tyHMPthGZvhY"
shop_bot = telebot.TeleBot(API_TOKEN)

commands = ["Add to list", "Get from list", "Delete from list"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*commands)

user_data = {}


@shop_bot.message_handler(commands=["start"])
def start(message):
    shop_bot.reply_to(message, "Welcome to shopping bot!", reply_markup=keyboard)


@shop_bot.message_handler(content_types=["text"])
def command(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = [[], None, None]
    if message.text == "Add to list":
        user_data[message.chat.id][1] = "add"
        # current_operation = "add"
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


shop_bot.polling()
