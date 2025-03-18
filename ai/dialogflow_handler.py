# ai/dialogflow_handler.py
from google.cloud import dialogflow_v2 as dialogflow
from config import Config
import logging

session_client = dialogflow.SessionsClient()

def get_dialogflow_response(chat_id, message_text, language_code):
    """Get a response from Dialogflow based on the user's message."""
    try:
        session = session_client.session_path(Config.DIALOGFLOW_PROJECT_ID, chat_id)
        text_input = dialogflow.TextInput(text=message_text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text
    except Exception as e:
        logging.error(f"Error during Dialogflow detect_intent: {e}")
        return "Sorry, I couldn't process your request."