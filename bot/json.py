import json
import logging
import telegram
from flask import request
from config import Config 

bot = telegram.Bot(token=Config.TELEGRAM_BOT_TOKEN)

def handle_json(req):
    """Parses JSON request from Telegram webhook."""
    try:
        raw_data = req.get_data(as_text=True)  # ✅ Fixed indentation
        logging.info(f"Raw Data: {raw_data}")  # Debugging

        data = json.loads(raw_data)  # Convert to JSON manually
        logging.info(f"Parsed Data: {data}")  # Debugging

        # Ensure 'data' has the right structure
        if not isinstance(data, dict):
            raise ValueError("Webhook received non-dictionary JSON data.")

        # Validate the update object
        if "message" not in data:
            raise KeyError("'message' field is missing in the update.")

        update = telegram.Update.de_json(data, bot)

        # Ensure message exists
        if not update.message:
            raise ValueError("Update has no message field.")

        chat_id = update.message.chat.id
        message_text = update.message.text if update.message.text else "No text message"

        logging.info(f"Chat ID: {chat_id}, Message: {message_text}")

        return data  # ✅ Return parsed JSON instead of HTTP response

    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {e}")
        return None  # ✅ Return None instead of HTTP error

    except KeyError as e:
        logging.error(f"Missing expected field: {e}")
        return None  # ✅ Return None instead of HTTP error

    except Exception as e:
        logging.error(f"Error handling webhook: {e}")
        return None  # ✅ Return None instead of HTTP error
