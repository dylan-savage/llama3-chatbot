from flask import Flask, request, jsonify
from llama3 import EmpathyBot
from flask_cors import CORS

# Set to True if you want to use the fine-tuned model
USE_FINE_TUNED_MODEL = False

app = Flask(__name__)
CORS(app, resources={
    r"/chat": {
        "origins": "http://localhost:3000",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"]
    }
}, supports_credentials=True)

bot = None

def initialize_bot():
    global bot
    try:
        if bot is None:
            bot = EmpathyBot(use_finetuned_model=USE_FINE_TUNED_MODEL)
        return True
    except Exception as e:
        print(f"Failed to initialize bot: {str(e)}")
        return False

@app.after_request
def after_request(response):
    print("CORS headers:", response.headers)
    return response

@app.route('/chat', methods=['POST'])
def chat():
    if not initialize_bot():
        return jsonify({'error': 'Failed to initialize the chatbot'}), 500
        
    try:
        data = request.json
        user_message = data.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
            
        result = bot.generate_response(user_message)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting server...")
    initialize_bot()
    app.run(debug=True, host='0.0.0.0', port=5050)
