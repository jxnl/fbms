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
        pass

    def comment(message):
        pass

    def get_number_of_likes():
        pass

    def get_number_of_comments():
        pass

    def __repr__(self):
        return self.id


class Group(DotAccess):

    def posts(self, limit=100, all=False):
        source, edge = self.id, "feed"
        for post in lazygen(Post, source, edge, limit=limit, get_all=all):
            yield post


class User(object):

    def groups(self, limit=100, all=False):
        source, edge = "me", "groups"
        for group in lazygen(Group, source, edge, limit=limit, get_all=all):
            yield group


if __name__ == "__main__":
    mark = User()
    for group in mark.groups(2):
        print group.name
        for post in group.posts(2):
            print post
