import json
import os

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


def load_json_file() -> list:
    try:
        with open("./data/blogs.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_file(data: list[dict]) -> bool:
    try:
        with open("./data/blogs.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def load_page(template_name: str, args=None):
    if args is None:
        args = {}
    return render_template(f'{template_name}.html', **args)


@app.route('/', endpoint="home")
def hello_world():
    blog_posts = load_json_file()
    args = {
        "posts": blog_posts
    }
    return load_page("index", args)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        store_new_post()
        return redirect(url_for('home'))

    return load_page('add')


def store_new_post():
    title = request.form.get('title', " ")
    author = request.form.get('author', " ")
    content = request.form.get('content', " ")

    blog_posts = load_json_file()

    new_id = max([post["id"] for post in blog_posts], default=0) + 1

    new_post = {
        "id": new_id,
        "author": author,
        "title": title,
        "content": content,
    }
    blog_posts.append(new_post)

    return write_file(blog_posts)


@app.route("/delete/<int:post_id>", endpoint="delete", methods=["GET"])
def delete(post_id: int):
    blog_posts = load_json_file()
    new_blog = [post for post in blog_posts if post["id"] != post_id]
    write_file(new_blog)
    return redirect(url_for("home"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        if uodate_post(post):
            return redirect(url_for("home"))
        else:
            return "Failed to write file."


    # Update the post in the JSON file
    # Redirect back to index

    # Else, it's a GET request
    # So display the update.html page
    args = {
        "title": post.get('title', " "),
        "author": post.get('author', " "),
        "content": post.get('content', " "),
    }
    return load_page("update", args)


def fetch_post_by_id(post_id: int) -> dict:
    blog_posts = load_json_file()
    return next((post for post in blog_posts if post["id"] == post_id), None)


def uodate_post(post: dict) -> bool:
    updated_title = request.form.get('title', post['title'])
    updated_author = request.form.get('author', post['author'])
    updated_content = request.form.get('content', post['content'])
    post['title'] = updated_title
    post['author'] = updated_author
    post['content'] = updated_content

    blog_posts = load_json_file()
    for idx, item in enumerate(blog_posts):
        if item['id'] == post['id']:
            blog_posts[idx] = post
            break

    return write_file(blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
