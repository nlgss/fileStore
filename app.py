# TOKEN = "7110090583:AAFIAXhX5HY7fJSqDspGIbZumZ4vXV0USlU"
# CHANNEL_ID = "-1002075467673"
# User = "1065291871"
import telebot
import asyncio
from telebot import types
from flask import Flask
from fuzzywuzzy import fuzz

# Telegram Bot Token
TOKEN = "6881144703:AAHpdcIbQlpLHzAOL4CBmQj8-HHfX0LBU8s"

# Telegram Channel ID
CHANNEL_ID = "-1002088156816"

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

linkList = {
    "DeAr 2024" : "https://nlgss.github.io/kaipulla/?val=4-5-6-7-8-9",
    "Rebel 2024" : "https://nlgss.github.io/kaipulla/?val=10-11-12-13-14-15",
    "Premalu 2024" : "https://nlgss.github.io/kaipulla/?val=16-17-18-19-20-21",
    "The family star 2024" : "https://nlgss.github.io/kaipulla/?val=22-23-24-25-26-27",
    "Siren 2024" : "https://nlgss.github.io/kaipulla/?val=28-29-30-31-32-33"
}

@bot.message_handler(commands=['start'])
def start(message):
    if len(message.text.split()) > 1:
        print(message.text.split()[1].split('-'))
        message_ids = message.text.split()[1].split('-')
        for message_id in message_ids:
            try:
                bot.forward_message(message.chat.id, CHANNEL_ID, message_id, disable_notification=True)
            except Exception as e:
                bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "Welcome to the Kaipulla File Storage Bot!")



# Handler for file uploads
@bot.message_handler(content_types=['document','video'])
def handle_file_upload(message):
    if message.from_user.id != 1065291871:
        return
    file_id = message.document.file_id if message.document else None
    if not file_id:
        return

    upload_response = bot.forward_message("-1002095805782", message.chat.id, message.message_id, disable_notification=True)
    upload_response = bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id, disable_notification=True)
    
    if upload_response:
        url = f"https://t.me/{bot.get_me().username}?start={upload_response.message_id}"
        bot.reply_to(message, f"File uploaded. Access it at: {url}")
    else:
        bot.reply_to(message, "Failed to upload file.")


@bot.message_handler(func=lambda message: message.chat.type == 'group')
def handle_group_messages(message):
    if message.content_type == 'text':
        results = []
        for key, value in linkList.items():
            similarity_key = fuzz.partial_ratio(message.text, str(key))
            results.append((key, value, similarity_key))

        results.sort(key=lambda x: x[2], reverse=True)
        markup = types.InlineKeyboardMarkup()
        for key, value, similarity in results[:5]:
            button = types.InlineKeyboardButton(text=key, url=value)
            markup.add(button)
            
        bot.reply_to(message, f'*Hello @{message.from_user.username}\nClick on a link below to get file\nIf requested file is not found, check spelling*', reply_markup=markup, parse_mode="Markdown")

@app.route('/')
def index():
    return make_response('', 200)

if __name__ == "__main__":
    bot_polling_task = asyncio.create_task(bot.polling())

    # Start the Flask web server asynchronously
    app.run(debug=True, port=8000)

    # Wait for both tasks to complete
    asyncio.get_event_loop().run_until_complete(bot_polling_task)
    
