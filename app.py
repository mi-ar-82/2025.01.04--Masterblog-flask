from flask import Flask, render_template, redirect, url_for, request
import json

app = Flask(__name__)


# Load blog posts from JSON file
def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

# Function to save blog posts to JSON
def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file)

@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch blog posts from JSON
    return render_template('index.html', posts=blog_posts)

#add post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Extract data from the form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing posts and generate a unique ID
        posts = load_posts()
        new_id = max(post['id'] for post in posts) + 1 if posts else 1

        # Create a new post dictionary
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}

        # Append the new post and save it back to the JSON file
        posts.append(new_post)
        save_posts(posts)

        # Redirect back to the home page
        return redirect(url_for('index'))

    # Render the form template for GET requests
    return render_template('add.html')

#delete post
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # Load existing posts
    posts = load_posts()

    # Filter out the post with the given ID
    posts = [post for post in posts if post['id'] != post_id]

    # Save the updated list of posts back to JSON
    save_posts(posts)

    # Redirect back to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
 