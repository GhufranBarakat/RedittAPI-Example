#import praw
import time
import urllib.parse

import json
import requests
from flask import Flask, request, jsonify, send_from_directory

MAX_RETRIES = 3
INITIAL_DELAY = 1  # Initial delay in seconds

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

'''reddit = praw.Reddit(client_id='***',
                     client_secret='***',
                     user_agent='***')'''

def make_request_with_retry(url, headers, params=None):
    delay = INITIAL_DELAY
    retries = 0
    
    while retries < MAX_RETRIES:
        response = requests.get(url, headers=headers, params=params)
        
        if response.ok:
            return response
        elif response.status_code == 429:
            # Rate limit exceeded, wait and retry
            delay *= 2  # Exponential backoff
            time.sleep(delay)
            retries += 1
        else:
            # Handle other errors
            return response
    
    # Max retries exceeded
    return None

# Define Reddit API endpoint
reddit_api_url = 'https://oauth.reddit.com'

@app.route('/popular', methods=['GET'])
def get_popular_subreddits():
    headers = {'Authorization': f"bearer {settings['access_token']}"}
    response = requests.get(f"{reddit_api_url}/subreddits/popular", headers=headers)
    if response.ok:
        popular_subs = [subreddit['data']['display_name_prefixed'] for subreddit in response.json()['data']['children']]
        return jsonify(popular_subs), 200
    else:
        return jsonify({'error': 'Failed to fetch popular subreddits'}), 500

@app.route('/posts', methods=['GET'])
def get_posts():
    subreddit_name = request.args.get('subreddit')
    if not subreddit_name:
        return jsonify({'error': 'Subreddit name is required'}), 400
    
    headers = {'Authorization': f"bearer {settings['access_token']}"}
    response = requests.get(f"{reddit_api_url}/r/{subreddit_name}/hot", headers=headers)
    
    try:
        response.raise_for_status()  # Raise an error for non-2xx status codes
        posts = [{'title': post['data']['title'], 'url': post['data']['url']} for post in response.json()['data']['children']]
        return jsonify(posts), 200
    except requests.HTTPError as e:
        app.logger.error(f"Error fetching posts: {e}")
        return jsonify({'error': 'Failed to fetch posts'}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/autocomplete', methods=['POST'])
def autocomplete_subreddits_post():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    headers = {'Authorization': f"bearer {settings['access_token']}"}
    params = {'q': query, 'type': 'sr'}
    response = make_request_with_retry(f"{reddit_api_url}/subreddits/search", headers=headers, params=params)
    
    try:
        if response is not None and response.ok:
            subreddits = [subreddit['data']['display_name'] for subreddit in response.json()['data']['children']]
            return jsonify(subreddits), 200
        else:
            return jsonify({'error': 'Failed to fetch autocomplete results'}), 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/submit', methods=['POST'])
def post_smth():
    url = "https://oauth.reddit.com/api/submit"
    data = {
        'title': 'Huuuuuuuuuuuh?',
        'kind': 'self',
        'sr': 'testing_some_calls',
        'resubmit': True,
        'sendreplies': True,
        'text': 'Test! ಠ_ಠ'
    }
    headers = {
        'Authorization': f'Bearer {settings.get("access_token")}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    encoded_payload = urllib.parse.urlencode(data)
    response = requests.request("POST", url, headers=headers, data=encoded_payload)
    #IDK what to return... response.json() throws 500 Error
    return "I guess it worked...", 200

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