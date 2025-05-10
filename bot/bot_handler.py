# bot/bot_handler.py
from flask import request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import Config
from database.firebase_handler import get_user_language, update_user_language, save_user_message
from ai.dialogflow_handler import get_dialogflow_response
from .file_sharing import handle_file_sharing
from .faq_handler import handle_faq
from .translate_text import translate_text
import logging
from .json import handle_json
import json

bot = telegram.Bot(token=Config.TELEGRAM_BOT_TOKEN)

def handle_user_message(update, context):
    """Process user messages and respond using Dialogflow."""
    chat_id = update.message.chat_id
    username = update.message.chat.username or "Unknown"
    user_message = update.message.text

    logging.info(f"📩 Received message from {chat_id}: {user_message}")

    # Get response from Dialogflow (or other AI system)
    response_text = get_dialogflow_response(user_message, chat_id)

    logging.info(f"🤖 Bot response: {response_text}")

    # ✅ Save to Firebase
    save_user_message(chat_id, username, user_message, response_text)

    # Send response back to the user
    context.bot.send_message(chat_id=chat_id, text=response_text)

def handle_translation(update, context):
    """Translate user message and respond in both languages."""
    user_text = update.message.text
    translated_data = translate_text(user_text, target_lang='am')

    # Reply in both languages
    response = f"🔹 Original: {translated_data['original']}\n🔹 Translated: {translated_data['translated']}"
    update.message.reply_text(response)

def handle_webhook():
    try:
        data = request.get_json(force=True)
        logging.info(f"Received webhook data: {json.dumps(data, indent=2)}")

        update = telegram.Update.de_json(data, bot)

        if not update.message:
            logging.error("Received an update without a message")
            return 'error', 400

        chat_id = update.message.chat.id
        username = update.message.chat.username or "Unknown"
        message_text = update.message.text if update.message.text else ""

        logging.info(f"Processing message from {username} ({chat_id}): '{message_text}'")

        if not message_text.strip():
            logging.error("Received a message with empty text")
            bot.send_message(chat_id=chat_id, text="I couldn't understand your message.")
            return 'error', 400

        if update.message.document or update.message.photo or update.message.video:
            handle_file_sharing(update, bot)
            return 'ok', 200

        # Check FAQ first
        faq_response = handle_faq(message_text)
        if faq_response:
            bot.send_message(chat_id=chat_id, text=faq_response)
            # Save FAQ interaction
            save_user_message(chat_id, username, message_text, faq_response)
            return 'ok', 200

        # Get user's language preference
        user_language = get_user_language(chat_id)
        logging.info(f"User {username} language preference: {user_language}")

        # Handle translation if needed
        if user_language == 'am':
            translation_result = translate_text(message_text, target_lang='en')
            if translation_result is None:
                bot.send_message(chat_id=chat_id, 
                               text="Sorry, I'm having trouble with translation right now. Please try again later.")
                return 'error', 500
            translated_text = translation_result['translated']
        else:
            translated_text = message_text

        # Get response from Dialogflow
        response_text = get_dialogflow_response(chat_id, translated_text, user_language)
        logging.info(f"Dialogflow response: '{response_text}'")

        if not response_text.strip():
            response_text = "I don't understand. Can you try rephrasing?"

        # Translate response if needed
        if user_language == 'am':
            translation_result = translate_text(response_text, target_lang='am')
            if translation_result is None:
                bot.send_message(chat_id=chat_id, 
                               text="Sorry, I generated a response but couldn't translate it. Please try again.")
                return 'error', 500
            final_response = translation_result['translated']
        else:
            final_response = response_text

        # Save the interaction
        if not save_user_message(chat_id, username, message_text, final_response):
            logging.error("Failed to save message to Firebase")
            # Continue anyway, as this shouldn't affect the user experience

        bot.send_message(chat_id=chat_id, text=final_response)

    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        return 'error', 500

    return 'ok', 200
