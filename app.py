from flask import Flask, render_template, request, redirect
from storage import BlogManager


class BlogApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.blog_manager = BlogManager("data.json")

        self.app.route('/')(self.index)
        self.app.route('/add', methods=['GET', 'POST'])(self.add)
        self.app.route('/delete/<int:post_id>')(self.delete)
        self.app.route('/update/<int:post_id>',
                       methods=['GET', 'POST'])(self.update)

    def index(self):
        blog_posts = self.blog_manager.fetch_posts()
        return render_template('index.html', posts=blog_posts)

    def add(self):
        if request.method == 'POST':
            author = request.form.get('author')
            title = request.form.get('title')
            content = request.form.get('content')

            blog_posts = self.blog_manager.fetch_posts()
            max_id = max(post['id'] for post in
                         blog_posts) if blog_posts else 0

            new_post = {
                'id': max_id + 1,
                'author': author,
                'title': title,
                'content': content
            }

            blog_posts.append(new_post)

            self.blog_manager.update_storage(blog_posts)
            return redirect('/')

        return render_template('add.html')

    def delete(self, post_id):
        blog_posts = self.blog_manager.fetch_posts()
        post = self.blog_manager.fetch_post_by_id(post_id)

        if post:
            blog_posts.remove(post)
            self.blog_manager.update_storage(blog_posts)
            return redirect('/')
        else:
            return "Post not found", 404

    def update(self, post_id):
        post_edit = self.blog_manager.fetch_post_by_id(post_id)
        blog_posts = self.blog_manager.fetch_posts()

        if post_edit:
            if request.method == 'POST':
                author = request.form.get('author')
                title = request.form.get('title')
                content = request.form.get('content')

                edited_text = {
                    'id': post_id,
                    'author': author,
                    'title': title,
                    'content': content
                }

                post_index = blog_posts.index(post_edit)
                blog_posts[post_index] = edited_text

                self.blog_manager.update_storage(blog_posts)
                return redirect('/')

            return render_template('update.html', post=post_edit,
                                   unedited_content=post_edit['content'])
        else:
            return "Post not found", 404

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    app = BlogApp()
    app.run()
