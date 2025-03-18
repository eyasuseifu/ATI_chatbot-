from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")

    response = ollama.chat(model="deepseek-coder", messages=[{"role": "user", "content": user_input}])
    
    return jsonify({"response": response["message"]["content"]})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
