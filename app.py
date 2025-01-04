from flask import Flask, render_template, redirect, url_for, request, flash
import json
import os

app = Flask(__name__)


# Load blog posts from JSON file
def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

# Function to save blog posts to JSON
def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file)
        
# Fetch a specific post by ID
def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch blog posts from JSON
    return render_template('index.html', posts=blog_posts)

#add post route
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

#delete post route
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

#update post route
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog post by ID
    print(f"Accessing update route for post_id: {post_id}")  # Debug: Verify correct ID
    posts = load_posts()
    print(f"Posts loaded: {posts}")  # Debug: Inspect loaded posts
    
    post = fetch_post_by_id(post_id)
    print(f"Post fetched for update: {post}")  # Debug: Check if the correct post is fetched
    
    if not post:
        print(f"Post with ID {post_id} not found!")  # Debug: Post not found case
        return "Post not found", 404

    if request.method == 'POST':
        print("Received POST request with data:", request.form)  # Debug: Inspect form data
        # Update the blog post with new data from the form
        for p in posts:
            if p['id'] == post_id:
                p['author'] = request.form.get('author')
                p['title'] = request.form.get('title')
                p['content'] = request.form.get('content')
                print(f"Updated post: {p}")  # Debug: Verify updated post
                break

        # Save updated posts back to JSON
        print(f"Posts list after update: {posts}")  # Debug: Check all posts before saving
        save_posts(posts)
        print("Posts saved successfully.")  # Debug: Confirm save

        # Redirect back to index page
        return redirect(url_for('index'))
    
    print(f"Rendering update form for post: {post}")  # Debug: Check data sent to the form
    # Render update form with current post data for GET requests
    return render_template('update.html', post=post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
 