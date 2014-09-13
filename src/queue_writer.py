import facebook
import requests

import datetime
from datetime import timedelta

import dateutil.parser

class QueueWriter:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)

    def write(self, queue):
        pass
