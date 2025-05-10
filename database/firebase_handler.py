# database/firebase_handler.py
import firebase_admin
from firebase_admin import credentials, firestore
import logging
import os
from pathlib import Path

# Initialize Firebase with better path handling
if not firebase_admin._apps:
    try:
        # Look for credentials file in the project root
        cred_path = Path(__file__).parent.parent / 'firebase-credentials.json'
        if not cred_path.exists():
            raise FileNotFoundError(f"Firebase credentials file not found at {cred_path}")
        cred = credentials.Certificate(str(cred_path))
        firebase_admin.initialize_app(cred)
        logging.info("✅ Firebase initialized successfully")
    except Exception as e:
        logging.error(f"❌ Failed to initialize Firebase: {e}")
        raise

db = firestore.client()

def get_user_language(chat_id):
    """Fetch the user's language preference from Firestore."""
    try:
        user_ref = db.collection('users').document(str(chat_id))
        user_data = user_ref.get()
        if not user_data.exists:
            logging.info(f"Creating new user document for chat_id: {chat_id}")
            user_ref.set({'language': 'en'})
            return 'en'
        return user_data.to_dict().get('language', 'en')
    except Exception as e:
        logging.error(f"Error getting user language: {e}")
        return 'en'  # Default to English on error

def update_user_language(chat_id, language):
    """Update the user's language preference in Firestore."""
    try:
        user_ref = db.collection('users').document(str(chat_id))
        user_ref.set({
            'language': language,
            'last_updated': firestore.SERVER_TIMESTAMP
        }, merge=True)
        logging.info(f"✅ Updated language for {chat_id} to {language}")
        return True
    except Exception as e:
        logging.error(f"❌ Error updating language: {e}")
        return False

def get_crop_info(crop_name):
    """Fetch crop information from Firestore."""
    doc_ref = db.collection("Crops").document(crop_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("info", "No data available for this crop.")
    else:
        return "Crop not found in the database."

def handle_intent(intent_name):
    """Handle user intents and return appropriate responses."""
    if intent_name.startswith("Crop-"):
        crop_name = intent_name.replace("Crop-", "")  # Extract crop name
        return get_crop_info(crop_name)
    return "I'm still learning! Please ask about Ethiopian crops."

def save_user_message(chat_id, username, message_text, response_text):
    """Save user message and bot response to Firestore."""
    try:
        if not all([chat_id, username, message_text, response_text]):
            raise ValueError("Missing required fields for saving message")

        message_ref = db.collection('messages').document(str(chat_id))
        message_data = {
            "username": username,
            "chat_id": str(chat_id),
            "messages": firestore.ArrayUnion([{
                "user_message": message_text,
                "bot_response": response_text,
                "timestamp": firestore.SERVER_TIMESTAMP
            }])
        }
        
        message_ref.set(message_data, merge=True)
        logging.info(f"✅ Successfully saved message for {chat_id}")
        return True
    except Exception as e:
        logging.error(f"❌ Error saving message: {e}")
        return False
