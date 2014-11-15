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

    props = []

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

    def persist(self, props=props):
        temp = {}
        temp["_id"] = self.data["id"]
        for prop in props:
            try:
                temp[prop] = self.data[prop]
            except KeyError:
                pass
        return temp


class Like(FBObject):

    def persist(self, props=None):
        temp = {}
        temp["from_id"] = self.data["id"]
        temp["from_name"] = self.data["name"]
        return temp


class Comment(FBObject):

    props = ["id", "like_count", "message", "created_time"]

    def like(self):
        """like this post"""
        User.graph().put_like(self.id)

    @property
    def user(self):
        return self.__dict__["from"]

    def _likes(self, limit=100, all=True):
        source, edge = self.id, "likes"
        return lazygen(Like, source, edge,
                       limit=limit, get_all=all)

    def persist(self, props=props):
        temp = super(Comment, self).persist(props)
        temp["from_name"] = self.data["from"]["name"]
        temp["from_id"] = self.data["from"]["id"]
        try:
            temp["message_tags"] = map(lambda p: int(p["id"]),
                                       self.data["message_tags"])
        except KeyError:
            pass
        return temp


class Post(FBObject):
    """Produces a generator of comments in this thread obj.comments()"""

    props = ["id", "message", "caption", "updated_time", "created_time",
             "like_count", "type"]

    def like(self):
        """like this post"""
        User.graph().put_like(self.id)

    @property
    def user(self):
        return self.__dict__["from"]

    @property
    def _id(self):
        return self.data["id"].split("_")[-1]

    def leave_comment(self, message):
        """leave a message on this post"""
        User.graph().put_comment(self.id, message)

    def _comments(self, limit=100, all=True):
        source, edge = self.id, "comments"
        return lazygen(Comment, source, edge,
                       limit=limit, get_all=all)

    def _likes(self, limit=100, all=True):
        source, edge = self.id, "likes"
        return lazygen(Like, source, edge,
                       limit=limit, get_all=all)

    def _delete(self):
        User.graph().delete_object(self.id)

    def persist(self, props=props):
        temp = super(Post, self).persist(props)
        try:
            temp["from_name"] = self.data["from"]["name"]
            temp["from_id"] = self.data["from"]["id"]
        except KeyError:
            pass
        try:
            temp["message_tags"] = map(lambda p: int(p["id"]),
                                       self.data["message_tags"]["0"])
        return temp


class Group(FBObject):
    """Produces a generator of posts in this thread obj.posts()"""

    props = ["id", "name"]

    def comment(self, message):
        """leave a message in this group"""
        User.graph().put_comment(self.id, message)

    def _posts(self, limit=100, all=True):
        """return an iterable of posts"""
        source, edge = self.id, "feed"
        return lazygen(Post, source, edge,
                       limit=limit, get_all=all)

    def persist(self, props=props):
        return super(Group, self).persist(props)


class Message(FBObject):

    @property
    def sender(self):
        return self.__dict__["from"].name


class InboxThread(FBObject):
    """Produces a generator of messages in this thread obj.messages()"""

    def messages(self, limit=10, all=True):
        source, edge = self.id, "comments"
        return lazygen(Message, source, edge,
                       limit=limit, get_all=all)
