from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import requests
import secrets
app = Flask(__name__)

import requests

FIREBASE_WEB_API_KEY = "AIzaSyDQ1lKKsrZbaxzgcYpBuu4wh8YEOvrEGHw"
# Secret key for session management
app.secret_key = secrets.token_hex(16)

# Firebase or other configs (optional, replace with real config)
config = {
    "apiKey": "AIzaSyDQ1lKKsrZbaxzgcYpBuu4wh8YEOvrEGHw",
    "authDomain": "grok-auth-d5feb.firebaseapp.com",
    "projectId": "grok-auth-d5feb",
    "storageBucket": "grok-auth-d5feb.appspot.com",
    "messagingSenderId": "1051029997965",
    "appId": "1:1051029997965:web:fdceb8733f5e854fd255c4",
    "measurementId": "G-6YJXE7M9G1"
}

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Firebase Auth API for login
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            user = response.json()
            session['user'] = user['email']  # Save user info in session
            return redirect(url_for('home'))
        else:
            error_message = response.json().get("error", {}).get("message", "Login failed!")
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Firebase Auth API for signup
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return redirect(url_for('login'))
        else:
            error_message = response.json().get("error", {}).get("message", "Signup failed!")
            return render_template('signup.html', error=error_message)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    message = data.get('message')

    # GROK API call
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer xai-g2IbdPu1O6jx9TfCaW9rJal7ai4lqbCWLJqNPkGZONP7yyS1JP7lMTJRz8GaHqd6V6PGCEYf8GXiF3yr',
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
