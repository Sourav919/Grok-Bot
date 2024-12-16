from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')

    # GROK API call
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xai-g2IbdPu1O6jx9TfCaW9rJal7ai4lqbCWLJqNPkGZONP7yyS1JP7lMTJRz8GaHqd6V6PGCEYf8GXiF3yr',  # Bearer added here
    }
    payload = {
        'messages': [
            {'role': 'system', 'content': 'You are a test assistant.'},
            {'role': 'user', 'content': message},
        ],
        'model': 'grok-beta',
        'stream': False,
        'temperature': 0,
    }
    response = requests.post('https://api.x.ai/v1/chat/completions', headers=headers, json=payload)
    
    # Check for errors in the response
    if response.status_code == 200:
        grok_reply = response.json().get('choices')[0].get('message').get('content')
        return jsonify({'reply': grok_reply})
    else:
        return jsonify({'error': 'Failed to get response from API', 'status_code': response.status_code}), 500

if __name__ == '__main__':
    app.run(debug=True)
