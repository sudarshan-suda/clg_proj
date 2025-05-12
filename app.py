from flask import Flask, render_template, request
import subprocess
import json
import os

app = Flask(__name__)
USERS_FILE = 'users.json'

# Load users from file
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pwd = request.form.get('password')
    users_db = load_users()
    if users_db.get(user) == pwd:
        subprocess.Popen(['python', 'm.py'])  # Launch YOLO detection
        return '<h2>Login successful. object detection started.</h2><a href="/">Back</a>'
    return '<h2>Invalid credentials.</h2><a href="/">Try again</a>'

@app.route('/register', methods=['POST'])
def register():
    user = request.form.get('username')
    pwd = request.form.get('password')
    confirm = request.form.get('confirm')
    users_db = load_users()

    if not user or not pwd:
        return '<h2>All fields are required.</h2><a href="/">Try again</a>'
    if pwd != confirm:
        return '<h2>Passwords do not match.</h2><a href="/">Try again</a>'
    if user in users_db:
        return '<h2>User already exists.</h2><a href="/">Try again</a>'

    users_db[user] = pwd
    save_users(users_db)
    return '<h2>Registered successfully. You can now login.</h2><a href="/">Back to login</a>'

if __name__ == '__main__':
    app.run(debug=True)
