# main.py
from flask import Flask
from bot.bot_handler import handle_webhook
from utils.logging_utils import setup_logging

app = Flask(__name__)
setup_logging()

@app.route('/webhook', methods=['POST'])
def webhook():
    return handle_webhook()

if __name__ == '__main__':
    app.run(port=5000)
    