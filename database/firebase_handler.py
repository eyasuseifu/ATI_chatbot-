# database/firebase_handler.py
import firebase_admin
from firebase_admin import credentials, firestore
from config import Config

# Initialize Firebase
cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_user_language(chat_id):
    """Fetch the user's language preference from Firestore."""
    user_ref = db.collection('users').document(str(chat_id))
    user_data = user_ref.get()
    return user_data.to_dict().get('language', 'en') if user_data.exists else 'en'

def update_user_language(chat_id, language):
    """Update the user's language preference in Firestore."""
    user_ref = db.collection('users').document(str(chat_id))
    user_ref.update({'language': language})

def get_crop_info(crop_name):
    """Fetch crop information from Firestore."""
    doc_ref = db.collection("Crops").document(crop_name)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("info", "No data available for this crop.")
    else:
        return "Crop not found in the database."
def handle_intent(intent_name, user_message):
    if intent_name.startswith("Crop-"):
        crop_name = intent_name.replace("Crop-", "")  # Extract crop name
        return get_crop_info(crop_name)
    return "I'm still learning! Please ask about Ethiopian crops."
