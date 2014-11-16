# -*- coding: utf-8 -*-

"""
marksweep.user
~~~~~~~~~~~~~~

This module contains User() which models the basic actions a user can go over the Facebook Graph API.

:author: Jason Liu (University of Waterloo)

In the future we will need to be able to handle connection pools if we want to crawl more intensely
While not all endpoints have been implemented, a user instance can get all groups, and all inbox messages
from the Graph API along with posting a status to their news feed.
"""

__author__ = 'JasonLiu'

from fbobject import *
from time import sleep, time
from config import APP_SECRET, APP_ID, ACCESS_TOKEN
from utils import lazygen
from facebook import GraphAPI


class User(object):

    call_counter = 0
    __graph = GraphAPI(ACCESS_TOKEN)

    @classmethod
    def graph(cls):
        cls.call_counter += 1
        if cls.call_counter > 600 and cls._time_since_last_nap() > 600:
            sleep(60)
            User.timer = time()
            cls.call_counter = 0
        return User.__graph

    def __init__(self):
        User.__graph.extend_access_token(APP_ID, APP_SECRET)
        User.timer = time()

    @staticmethod
    def update_status(message):
        User.graph.put_object("me", "feeds", message)

    # @staticmethod
    # def inbox(limit=100, all=True):
    #     source, edge = "me", "inbox"
    #     return lazygen(InboxThread, source, edge, limit, all)

    @staticmethod
    def groups(limit=100, all=True):
        source, edge = "me", "groups"
        return lazygen(Group, source, edge, limit, all)

    @classmethod
    def _time_since_last_nap(cls):
        # noinspection PyUnresolvedReferences
        return time() - cls.timer
