# bot/faq_handler.py
import logging
from database.firebase_handler import db

def handle_faq(message_text: str):
    """
    Checks if the user's message matches any FAQ in the database
    and returns the response if a match is found.
    """
    try:
        # Access the 'faqs' collection in Firestore
        faqs_ref = db.collection('faqs')
        faq_docs = faqs_ref.stream()

        for faq in faq_docs:
            faq_data = faq.to_dict()
            question = faq_data.get('question').lower()
            response = faq_data.get('response')

            # Check if the user's message matches the FAQ question
            if question in message_text.lower():
                logging.info(f"FAQ match found for question: {question}")
                return response

        logging.info("No FAQ match found.")
        return None  # No match found

    except Exception as e:
        logging.error(f"Error handling FAQ: {e}")
        return None