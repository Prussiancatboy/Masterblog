import json


class BlogManager:
    def __init__(self, data_file):
        self.data_file = data_file

    def fetch_posts(self):
        """Fetches posts from the JSON file."""
        with open(self.data_file) as fileobj:
            blog_posts = json.load(fileobj)
        return blog_posts

    def fetch_post_by_id(self, post_id):
        """Searches for a post by its ID and retrieves it."""
        blog_posts = self.fetch_posts()
        for post in blog_posts:
            if post["id"] == post_id:
                return post
        return None

    def update_storage(self, data):
        """Updates the JSON file with the provided data."""
        with open(self.data_file, 'w') as file:
            json.dump(data, file)
