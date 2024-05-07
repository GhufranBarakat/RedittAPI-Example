function getPopularSubreddits() {
    fetch('/popular')
        .then(response => response.json())
        .then(data => {
            const popularSubreddits = document.getElementById('popularSubreddits');
            popularSubreddits.innerHTML = data.join('<br>');
        })
        .catch(error => console.error('Error:', error));
}

function getPosts() {
    const subreddit = document.getElementById('subredditInput').value;
    fetch(`/posts?subreddit=${subreddit}`)
        .then(response => response.json())
        .then(data => {
            const posts = document.getElementById('posts');
            posts.innerHTML = '';
            data.forEach(post => {
                posts.innerHTML += `<p><a href="${post.url}">${post.title}</a></p>`;
            });
        })
        .catch(error => console.error('Error:', error));
}

function autocomplete() {
    const query = document.getElementById('autocompleteInput').value;
    const body = {
        query: query,
        exact: false,
        include_over_18: false
    };
    fetch('/autocomplete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        const autocompleteResults = document.getElementById('autocompleteResults');
        autocompleteResults.innerHTML = data.join('<br>');
    })
    .catch(error => console.error('Error:', error));
}
  

// to continue