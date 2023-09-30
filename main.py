import telebot


API_TOKEN = "6454697652:AAEBf2IBBK4NUsJ0jqtyHW4tyHMPthGZvhY"
shop_bot = telebot.TeleBot(API_TOKEN)

commands = ["Add to list", "Get from list", "Delete from list"]
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row(*commands)

shopping_list = []
current_operation = None
last_message_id = None

@shop_bot.message_handler(commands=["start"])
def start(message):
    shop_bot.reply_to(message, "Welcome to shopping bot!", reply_markup=keyboard)


@shop_bot.message_handler(content_types=["text"])
def command(message):
    global current_operation
    global shopping_list
    global last_message_id
    if message.text == "Add to list":
        current_operation = "add"
        shop_bot.reply_to(message, "You can add items to the list")
    elif message.text == "Get from list":
        current_operation = "get"
        shop_bot.reply_to(message, ", ".join(shopping_list) if shopping_list else "Your shopping list is empty")
    elif message.text == "Delete from list":
        current_operation = "del"
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        for elem in shopping_list:
            inline_keyboard.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
        res = shop_bot.reply_to(message, "Delete items", reply_markup=inline_keyboard)
        last_message_id = res.message_id
    else:
        if current_operation == "add":
            shopping_list.append(message.text)
            shop_bot.reply_to(message, f"Successfully added {message.text}")


@shop_bot.callback_query_handler(func=lambda x: True)
def callback_handler(call):
    global shopping_list
    for i in range(len(shopping_list)):
        if shopping_list[i] == call.data:
            del shopping_list[i]
            break
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    for elem in shopping_list:
        inline_keyboard.add(telebot.types.InlineKeyboardButton(elem, callback_data=elem))
    shop_bot.edit_message_reply_markup(call.message.chat.id, last_message_id, reply_markup=inline_keyboard)


shop_bot.polling()
