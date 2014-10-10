# -*- coding: utf-8 -*-

"""
marksweep.fbobject
~~~~~~~~~~~~~~~~~~~~~

this module contains the classes and methods required to simulate a
facebook user.
"""

import json
from user import *
from utils import lazygen


class FBObject(object):

    @classmethod
    def dot_access(cls, obj, dic):
        """Unpythonic way to turn everything into a dot accessed object """
        for k in dic.keys():
            v = dic.get(k)
            if isinstance(v, dict):
                obj.__setattr__(str(k), cls(v))
            else:
                obj.__setattr__(str(k), v)
        return obj

    def __init__(self, data):
        self.data = data
        self.dot_access(self, self.data)

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self, *args, **kwargs):
        return json.dumps(self.data, *args, **kwargs)

    def _pprint(self):
        print json.dumps(self.data, indent=4)


class Comment(FBObject):

    def like(self):
        """like this post"""
        User.graph().put_like(self.id)

    @property
    def user(self):
        return self.__dict__["from"]


class Post(FBObject):
    """Produces a generator of comments in this thread obj.comments()"""

    def like(self):
        """like this post"""
        User.graph().put_like(self.id)

    @property
    def user(self):
        return self.__dict__["from"]

    def leave_comment(self, message):
        """leave a message on this post"""
        User.graph().put_comment(self.id, message)

    def get_likes(self):
        """get the of likes on this post"""
        source, edge = self.id, "likes"
        return User.graph().get_connections(source, edge, limit=100000)["data"]

    def comments(self, limit=100, all=False):
        """return an iterable of posts"""
        source, edge = self.id, "comments"
        return lazygen(Comment, source, edge,
                       limit=limit, get_all=all)

    def _delete(self):
        User.graph().delete_object(self.id)


class Group(FBObject):
    """Produces a generator of posts in this thread obj.posts()"""

    def comment(self, message):
        """leave a message in this group"""
        User.graph().put_comment(self.id, message)

    def posts(self, limit=100, all=False):
        """return an iterable of posts"""
        source, edge = self.id, "feed"
        return lazygen(Post, source, edge,
                       limit=limit, get_all=all)


class Message(FBObject):

    @property
    def sender(self):
        return self.__dict__["from"].name


class InboxThread(FBObject):
    """Produces a generator of messages in this thread obj.messages()"""

    def messages(self, limit=10, all=False):
        source, edge = self.id, "comments"
        return lazygen(Message, source, edge,
                       limit=limit, get_all=all)
