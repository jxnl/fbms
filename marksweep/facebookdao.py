# -*- coding: utf-8 -*-

"""
marksweep.facebookdao
~~~~~~~~~~~~~~~~~~~~~

this module contains the classes and methods required to simulate a
facebook user.
"""

from utils import lazygen, DotAccess


class Post(DotAccess):

    def like():
        """like this post"""
        pass

    def comment(message):
        """leave a message on this post"""
        pass

    def get_likes():
        """get the set of likes on this post"""
        pass

    def get_comments():
        """get the set of likes on this post"""
        pass

    def _delete():
        """try to delete this post"""
        pass

    def __repr__(self):
        return self.id


class Group(DotAccess):

    def comment(message):
        """leave a message in this group"""
        pass

    def posts(self, limit=100, all=False):
        """return an iterable of posts"""
        source, edge = self.id, "feed"
        for post in lazygen(Post, source, edge, limit=limit, get_all=all):
            yield post


class User(object):

    def check_user(id):
        """obtain the profile of these users"""
        pass

    def update_status(message):
        """update the users status"""
        pass

    def groups(self, limit=100, all=False):
        """return an interable of groups"""
        source, edge = "me", "groups"
        for group in lazygen(Group, source, edge, limit=limit, get_all=all):
            yield group


if __name__ == "__main__":
    mark = User()
    for group in mark.groups(2):
        print group.name
        for post in group.posts(2):
            print post
