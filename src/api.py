import praw
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

reddit = praw.Reddit(client_id='***',
                     client_secret='***',
                     user_agent='***')

# Serve the static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Serve the HTML file
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(port=5000)