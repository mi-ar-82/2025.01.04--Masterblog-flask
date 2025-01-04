from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)


# Load blog posts from JSON file
def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch blog posts from JSON
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
 