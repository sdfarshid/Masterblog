import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():

    with open("./data/blogs.json", "r", encoding="utf-8") as file:
        blog_posts = json.load(file)

    print(blog_posts)
    return render_template("index.html", posts=blog_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)