function getPopularSubreddits() {
  fetch('/popular')
    .then(response => response.json())
    .then(data => {
        const popularSubreddits = document.getElementById('popularSubreddits');
        if (Array.isArray(data)) {
            popularSubreddits.innerHTML = data.join('<br>');
        } else {
            popularSubreddits.innerHTML = "Error: Data is not an array";
        }
    })
    .catch(error => console.error('Error:', error));
}

function getPosts() {
  const subreddit = document.getElementById('subredditInput').value.trim();

  if (!subreddit) {
    alert('Please enter a subreddit name.');
    return;
  }

  fetch(`/posts?subreddit=${subreddit}`)
    .then(response => response.json())
    .then(data => {
      const postsElement = document.getElementById('posts');
      postsElement.innerHTML = '';

      data.forEach(post => {
        const postElement = document.createElement('p'); // Create a new paragraph element for each post

        const postLink = document.createElement('a');
        postLink.href = post.url;
        postLink.textContent = post.title;

        postElement.appendChild(postLink); // Add the link to the paragraph
        postsElement.appendChild(postElement); // Add the paragraph to the posts container
      });
    })
    .catch(error => console.error('Error:', error));
}

function autocomplete() {
  const query = document.getElementById('autocompleteInput').value;
  fetch('/autocomplete', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: query })
  })
    .then(response => response.json())
    .then(data => {
      const autocompleteResults = document.getElementById('autocompleteResults');
      autocompleteResults.innerHTML = '';
      if (Array.isArray(data)) {
          data.forEach(result => {
              autocompleteResults.innerHTML += `<p>${result}</p>`;
          });
      } else {
          autocompleteResults.innerHTML = "Error: Data is not an array";
      }
    })
    .catch(error => console.error('Error:', error));
}
  
function createPost() {
  const titleInput = document.querySelector('input.post_obj');
  const textArea = document.querySelector('textarea.post_obj');

  const data = {
      'title': titleInput.value,
      'kind': 'self',
      'sr': 'APITest_SWA',
      'resubmit': true,
      'sendreplies': true,
      'text': textArea.value
  };

  fetch('/submit', {
      method: "POST",
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
}

function addFriend() {
  const username = document.querySelector('.input_fields').value.trim();

  if(!username){
    alert('enter a username!');
    return
  }

  fetch('/friend', {
    method: "PUT",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: username})
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => console.error('Error:', error));
}

function removeFriend() {
  const username = document.querySelector('.remove_fields').value.trim();

  if (!username) {
    alert('enter a username!');
    return;
  }

  fetch('/unfriend', {
    method: "DELETE",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: username })
  })
    .then(response => {
      if (response.ok) {
        alert('Erfolg! Freund entfernt.');
      } else {
        alert('Fehler: ' + response.statusText);
      }
    })
    .catch(error => console.error('Fehler:', error));
}

// to continue
