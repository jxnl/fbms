import facebook
import time

from fbobject import *
from config import APP_SECRET, APP_ID, ACCESS_TOKEN
from utils import lazygen


class User(object):

    call_counter = 0
    __graph = facebook.GraphAPI(ACCESS_TOKEN)

    @classmethod
    def graph(cls):
        """return the graph object and watch rate limiting"""
        cls.call_counter += 1
        if User._time_since_last_nap > 600 and cls.call_counter > 600:
            time.sleep(10)
            User.timer = time.time()
        return User.__graph

    def __init__(self):
        User.__graph.extend_access_token(APP_ID, APP_SECRET)
        User.timer = time.time()

    def update_status(self, message):
        """update the users status"""
        User.graph.put_object("me", "feeds", message)

    def inbox(self, limit=100, all=False):
        source, edge = "me", "inbox"
        return lazygen(InboxThread, source, edge, limit, all)

    def groups(self, limit=100, all=False):
        """return an interable of groups"""
        source, edge = "me", "groups"
        return lazygen(Group, source, edge, limit, all)

    def _time_since_last_nap():
        return User.timer - time.time()
