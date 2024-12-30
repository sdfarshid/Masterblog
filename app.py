import json
import os

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


def load_json_file() -> list:
    if os.stat("./data/blogs.json").st_size == 0:
        contents = []
    else:
        with open("./data/blogs.json", "r", encoding="utf-8") as file:
            contents = json.load(file)
    return contents


def write_file(data: list[dict]):
    with open("./data/blogs.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@app.route('/', endpoint="home")
def hello_world():
    blog_posts = load_json_file()

    print(blog_posts)
    return render_template("index.html", posts=blog_posts)


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

    write_file(blog_posts)



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        store_new_post()
        return redirect(url_for('home'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
