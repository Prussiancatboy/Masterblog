from flask import Flask, render_template, request, redirect
import storage


def main():
    app = Flask(__name__)

    @app.route('/')
    def index():
        """This makes the webpage, and indexes it"""
        blog_posts = storage.fetch_posts()
        return render_template('index.html', posts=blog_posts)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        """This code allows you to add things"""

        if request.method == 'POST':
            # Retrieve the form data from the request
            author = request.form.get('author')
            title = request.form.get('title')
            content = request.form.get('content')

            # Retrieve the entire form
            blog_posts = storage.fetch_posts()

            # This code gets the max number from id
            max_id = max(post['id'] for post in blog_posts) \
                if blog_posts else 0

            # This code creates a new post dictionary with id
            new_post = {
                'id': max_id + 1,
                'author': author,
                'title': title,
                'content': content
            }

            blog_posts.append(new_post)

            storage.update_storage(blog_posts)
            return redirect('/')

        return render_template('add.html')

    @app.route('/delete/<int:post_id>')
    def delete(post_id):
        """This code allows you to delete things"""

        blog_posts = storage.fetch_posts()

        for id_dict in blog_posts:
            if id_dict["id"] == post_id:
                blog_posts.remove(id_dict)
                break

        storage.update_storage(blog_posts)

        return redirect('/')

    @app.route('/update/<int:post_id>', methods=['GET', 'POST'])
    def update(post_id):
        """This code allows you to update things"""

        # this stores the text to add on
        edited_text = {}

        # this fetches the post and index
        post_edit, post_index = storage.fetch_post_by_id(post_id)
        blogposts = storage.fetch_posts()
        if post_edit is None:
            # Post not found
            return "Post not found", 404

        if request.method == 'POST':
            # Retrieve the form data from the request
            author = request.form.get('author')
            title = request.form.get('title')
            content = request.form.get('content')

            # this makes a new dictionary
            edited_text['id'] = post_id
            edited_text['author'] = author
            edited_text['title'] = title
            edited_text['content'] = content

            # this deletes the old dictionary
            del blogposts[post_index]

            # adds the new dictionary to the list
            blogposts.append(edited_text)

            # and finally this updates the list
            storage.update_storage(blogposts)

            return redirect('/')

        # Else, it's a GET request
        # So display the update.html page
        return render_template('update.html', post=post_edit,
                               unedited_content=post_edit['content'])

    if __name__ == '__main__':
        app.run(debug=True)

if __name__ == '__main__':
    main()
