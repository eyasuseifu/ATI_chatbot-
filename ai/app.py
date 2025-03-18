# app.py
from flask import Flask, request, jsonify
from bot.bot_handler import handle_webhook  # Import handle_webhook from bot_handler

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    return handle_webhook()  # Call the function from bot_handler

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Run the Flask app
