from flask import Flask, render_template
import json


def hold():
    app = Flask(__name__)
    @app.route('/')
    def index():
        with open("data.json") as fileobj:
            blog_posts = json.load(fileobj)
        return render_template('index.html', posts=blog_posts[0])

    if __name__ == '__main__':
        app.run()

hold()