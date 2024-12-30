from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Define a simple route
@app.route('/')
def home():
    return "Welcome to the GPT-3 AI Chatbot Backend!"

# Define an endpoint for the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    # Placeholder response (GPT-3 integration will go here later)
    bot_response = f"You said: {user_message}"
    return jsonify({'response': bot_response})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

