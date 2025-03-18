# bot/file_sharing.py
import logging
import requests
from telegram import Update
from config import Config
from database.firebase_handler import db
from firebase_admin import storage

def handle_file_sharing(update: Update, bot):
    """Handles document, photo, and video sharing by users."""
    chat_id = update.message.chat.id

    try:
        # Check if the message contains a document
        if update.message.document:
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name
            logging.info(f"Received file: {file_name} from chat_id: {chat_id}")

            # Download the file from Telegram
            file_path = download_file_from_telegram(bot, file_id, file_name, Config.TELEGRAM_BOT_TOKEN)

            # Optional: Upload to Firebase Storage
            upload_to_firebase(file_path, file_name)

            # Send response to the user
            bot.send_message(chat_id=chat_id, text=f"File {file_name} received and stored.")

        # Handle photo uploads
        elif update.message.photo:
            file_id = update.message.photo[-1].file_id  # Get the highest resolution photo
            logging.info(f"Received photo from chat_id: {chat_id}")

            # Download the photo from Telegram
            file_path = download_file_from_telegram(bot, file_id, 'photo.jpg', Config.TELEGRAM_BOT_TOKEN)

            # Send response to the user
            bot.send_message(chat_id=chat_id, text="Photo received and stored.")

        # Handle video uploads
        elif update.message.video:
            file_id = update.message.video.file_id
            logging.info(f"Received video from chat_id: {chat_id}")

            # Download the video from Telegram
            file_path = download_file_from_telegram(bot, file_id, 'video.mp4', Config.TELEGRAM_BOT_TOKEN)

            # Send response to the user
            bot.send_message(chat_id=chat_id, text="Video received and stored.")

    except Exception as e:
        logging.error(f"Error handling file sharing: {e}")
        bot.send_message(chat_id=chat_id, text="There was an error handling your file.")

def download_file_from_telegram(bot, file_id, file_name, telegram_token):
    """Download file from Telegram and store locally."""
    file = bot.get_file(file_id)
    file_path = file.file_path
    file_url = f"https://api.telegram.org/file/bot{telegram_token}/{file_path}"
    response = requests.get(file_url)

    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        logging.info(f"File {file_name} downloaded successfully.")
        return file_name
    else:
        logging.error(f"Failed to download file {file_name} from Telegram.")
        return None

def upload_to_firebase(file_path, file_name):
    """Upload the downloaded file to Firebase Storage."""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        logging.info(f"File {file_name} uploaded to Firebase Storage.")
    except Exception as e:
        logging.error(f"Error uploading file to Firebase: {e}")