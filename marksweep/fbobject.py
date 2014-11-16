# -*- coding: utf-8 -*-

"""
marksweep.fbobject
~~~~~~~~~~~~~~~~~~

This module contains the classes and methods required to simulate a
facebook user.
"""

__author__ = 'JasonLiu'

from json import dumps
from facebook_user import *
from utils import lazygen


class FBObject(object):
    props = []

    @classmethod
    def dot_access(cls, obj, dic):
        """
        Unpythonic way to turn everything into a dot accessed object!

        :param obj:
        :param dic:
        :return:
        """
        for k in dic.keys():
            v = dic.get(k)
            if isinstance(v, dict):
                obj.__setattr__(str(k), cls(v))
            else:
                obj.__setattr__(str(k), v)
        return obj

    def _pprint(self):
        """
        Pretty print object as it's full json
        """
        print dumps(self.data, indent=4)

    def persist(self, props=props):
        """
        Convert this object into a dictinoary that MongoDB can persist

        :param props:
        :return:
        """
        persistable_dict = {"_id": self.data["id"]}
        for prop in props:
            try:
                persistable_dict[prop] = self.data[prop]
            except KeyError:
                pass
        return persistable_dict

    def __init__(self, data):
        self.data = data
        self.dot_access(self, self.data)

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self, *args, **kwargs):
        return dumps(self.data, *args, **kwargs)


class Like(FBObject):
    def persist(self, props=None):
        """
        Convert this object into a dictinoary that MongoDB can persist

        :param props:
        :return:
        """
        persistable_dict = {"from_id": self.data["id"], "from_name": self.data["name"]}
        return persistable_dict


class Comment(FBObject):
    props = ["id", "like_count", "message", "created_time"]

    def like(self):
        """
        Like this comment
        """
        User.graph().put_like(self.id)

    @property
    def user(self):
        """
        Returns a dict that maps "id" and "name"
        """
        return self.__dict__["from"]

    def likes_(self, limit=100, all=True):
        """
        Return a lazy generator of Like objects

        :param limit:
        :param all:
        :return:
        """
        source, edge = self.id, "likes"
        return lazygen(
            Like, source, edge, limit=limit, get_all=all
        )

    def persist(self, props=props):
        """
        Convert this object into a dictinoary that MongoDB can persist

        :param props:
        :return:
        """
        persistable_dict = super(Comment, self).persist(props)
        try:
            persistable_dict["from_name"] = self.data["from"]["name"]
            persistable_dict["from_id"] = self.data["from"]["id"]
        except KeyError:
            pass
        try:
            persistable_dict["message_tags"] = map(
                lambda p: int(p["id"]), self.data["message_tags"]
            )
        except KeyError:
            pass
        return persistable_dict


class Post(FBObject):
    props = ["id", "message", "caption", "updated_time", "created_time", "like_count", "type"]

    def like(self):
        """
        Like this post
        """
        User.graph().put_like(self.id)

    @property
    def user(self):
        """
        :return: a dict that maps "id" and "name"
        """
        return self.__dict__["from"]

    @property
    def id_(self):
        """
        :return: facebook post id
        """
        return self.data["id"].split("_")[1]

    @property
    def group_id_(self):
        """
        :return: facebook group id of post
        """
        return self.data["id"].split("_")[0]

    def leave_comment(self, message):
        """
        Leave a message on this post
        """
        User.graph().put_comment(self.id, message)

    def comments_(self, limit=100, all=True):
        """
        :param limit:
        :param all:
        :return: Lazy generator of Comment Objects
        """
        source, edge = self.id, "comments"
        return lazygen(
            Comment, source, edge, limit=limit, get_all=all
        )

    def likes_(self, limit=100, all=True):
        """
        :param limit:
        :param all:
        :return: Lazy generator of Like Objects
        """
        source, edge = self.id, "likes"
        return lazygen(
            Like, source, edge, limit=limit, get_all=all
        )

    def delete_(self):
        """
        Try to Delete this post
        """
        User.graph().delete_object(self.id)

    def persist(self, props=props):
        """
        Convert this object into a dict that MongoDB can persist

        :param props:
        :return:
        """
        persistable_dict = super(Post, self).persist(props)
        try:
            persistable_dict["from_name"] = self.data["from"]["name"]
            persistable_dict["from_id"] = self.data["from"]["id"]
        except KeyError:
            pass
        try:
            persistable_dict["message_tags"] = map(
                lambda p: int(p["id"]), self.data["message_tags"]["0"]
            )
        except KeyError:
            pass
        return persistable_dict


class Group(FBObject):
    props = ["id", "name"]

    def comment(self, message):
        """
        Leave a message in this group
        """
        User.graph().put_comment(self.id, message)

    def posts_(self, limit=100, all=True):
        """
        :param limit:
        :param all:
        :return: Lazy generator of Post Objects
        """
        source, edge = self.id, "feed"
        return lazygen(
            Post, source, edge, limit=limit, get_all=all
        )

    def persist(self, props=props):
        """
        Convert this object into a dictinoary that MongoDB can persist

        :param props:
        :return:
        """
        return super(Group, self).persist(props)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Messages and InboxThreads are not supported at this time
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# class Message(FBObject):
#
#     @property
#     def sender(self):
#         return self.__dict__["from"].name
#
#
# class InboxThread(FBObject):
#
#     def messages(self, limit=1000, all=False):
#         source, edge = self.id, "comments"
#         return lazygen(
#             Message, source, edge, limit=limit, get_all=all
#             )
#

