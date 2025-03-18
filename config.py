# config.py
import os

class Config:
    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7280803753:AAGEV6ACz1O_sCpo4ayV6V9Aja1U-WqB7EE')

    # Dialogflow Configuration
    DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID', 'fine-transit-430509-g3')
    DIALOGFLOW_LANGUAGE_CODE = os.getenv('DIALOGFLOW_LANGUAGE_CODE', 'en')

    # Firebase Configuration
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH', r'C:\Users\HP\Documents\chat_bot2\chatbot-d8dac-firebase-adminsdk-q4u4b-e7c5779829.json')

    

    # Webhook URL
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', ' https://sweet-frogs-mate.loca.lt/webhook')
    
    #Google 
    GOOGLE_APPLICATION_CREDENTIALS = r"C:\\Users\\HP\\Documents\\chat_bot2\\fine-transit-430509-g3-06cfbd7067ed.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
