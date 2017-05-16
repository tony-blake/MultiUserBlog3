""" Google Datastore Database Model for a Blog Post Comment

    Properties:
        content: Comment content (str)
        author: Comment author (str)
        created: Date and time when comment was posted (DateTime)

    Class Methods:
        get_comments(parent) - Gets all comments for a specific blog post

    Methods:
        render() - Replaces newlines with <br> in comment content,
        and stores in variable self._render_text
"""

import webapp2

from google.appengine.ext import db


class Comment(db.Model):

    """ Database model for a user """
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_comments(cls, parent):
        """ Returns an array of Comment entities
        for a parent Blog post """
        comment_arry = []
        comments = cls.all().ancestor(parent)  # get all commentts for a post
        comments.order("-created")  # order from most to least recent

        for comment in comments:
            comment.render()  # replace newlines with <br>
            comment_arry.append(comment)

        return comment_arry

    @classmethod
    def get_by_id(cls, author, post_id, comment_id):
        """ Returns a comment entity
        corresponding to a post and comment id """
        key = db.Key.from_path("User", author,
                               "Post", int(post_id),
                               "Comment", int(comment_id))
        if key:
            return db.get(key)  # retrieve Comment entity form db key
        else:
            return False

    @classmethod
    def edit(cls, author, post_id, comment_id, content=None):
        """ Edits title and/or content of specified comment
        and writes changes to database """
        comment = cls.get_by_id(author, post_id, comment_id)
        if comment:
            if content:
                comment.content = content  # edit content if changed
            comment.put()
            return True
        return False

    @classmethod
    def delete(cls, author, post_id, comment_id):
        """ Deletes comment at key path: author, post_id, comment_id """
        db_key = db.Key.from_path("User", author,
                                  "Post", int(post_id),
                                  "Comment", int(comment_id))
        if db_key:
            db.delete(db_key)  # delete the entity matching db_key
            return True
        else:
            return False

    def render(self):
        """ Replaces newlines in post content with <br>
        and saves to self._render_text"""
        self._render_text = self.content.replace('\n', '<br>')
