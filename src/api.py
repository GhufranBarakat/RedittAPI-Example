import praw
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

reddit = praw.Reddit(client_id='***',
                     client_secret='***',
                     user_agent='***')

@app.route('/popular', methods=['GET'])
def get_popular_subreddits():
    popular_subs = []
    for subreddit in reddit.subreddits.popular(limit=10):
        popular_subs.append(subreddit.display_name_prefixed)
    return jsonify(popular_subs), 200

@app.route('/posts', methods=['GET'])
def get_posts():
    subreddit_name = request.args.get('subreddit')
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=10):
        posts.append({
            'title': post.title,
            'url': post.url
        })
    return jsonify(posts), 200

@app.route('/autocomplete', methods=['POST'])
def get_list_of_possible_subs():
    query = request.json['query']
    results = []
    for subreddit in reddit.subreddits.search(query):
        results.append(subreddit.display_name_prefixed)
    return jsonify(results), 200


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