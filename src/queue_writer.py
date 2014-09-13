import facebook
import requests

from sets import Set

import datetime
from datetime import timedelta

import dateutil.parser

class QueueWriter:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)
        self.ids_written = Set()

    # Get the top N (max_items) and write them to the set
    # Always write the ID to the {@link self.ids_written} set
    # If they exist prior, don't write and skip over.
    # Queue.push(item)
    # 
    # Don't parse into objects till later, should work fine
    def write(self, queue, max_items=30):
        posts = self.graph.get_connections(self.group_id, "feed")

        posts_added = 0

        while True:
            if 'paging' in posts:
                for post_raw in posts:
                    post_id = post_raw["id"].split("_")[1]
                    if not post_id in self.ids_written:
                        fb_post = facebook.FacebookPost(post_raw)

                        if fb_post and posts_added++ >= max_items:
                            self.ids_written.add(post_id)
                            queue.push(fb_post)
                        else:
                            return
                    else:
                        return
                posts = requests.get(posts['paging']['next']).json()
