# bot/bot_handler.py
from flask import request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from database.firebase_handler import get_user_language, update_user_language
from ai.dialogflow_handler import get_dialogflow_response
from .file_sharing import handle_file_sharing
from .faq_handler import handle_faq
from .translate_text import translate_text
import logging
from .json import handle_json

bot = telegram.Bot(token=Config.TELEGRAM_BOT_TOKEN)

def handle_webhook():
    try:
        
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        message_text = update.message.text

        # Handle file sharing
        if update.message.document or update.message.photo or update.message.video:
            handle_file_sharing(update, bot)
            return 'ok', 200

        # Handle FAQ queries
        faq_response = handle_faq(message_text)
        if faq_response:
            bot.send_message(chat_id=chat_id, text=faq_response)
            return 'ok', 200

        # Fetch user language preference
        user_language = get_user_language(chat_id)

        # Translate response if needed
        if user_language == 'am':
            message_text = translate_text(message_text, target_lang='am')

        # Process the message with Dialogflow
        response_text = get_dialogflow_response(chat_id, message_text, user_language)

        # Send the response back to the user
        bot.send_message(chat_id=chat_id, text=response_text)

    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        return 'error', 500

    return 'ok', 200