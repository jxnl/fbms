# -*- coding: utf-8 -*-

"""
marksweep.crawler-example
~~~~~~~~~~~~~~~~~~

"""

__author__ = 'JasonLiu'


import logging

import facebook_user
import datetime
import time
# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from pymongo import MongoClient


logging.basicConfig(filename="../logs/crawler.log",
                    level=logging.DEBUG)

if __name__ == "__main__":
    DAO = MongoClient().hackathonhackers
    LOG = logging.getLogger("crawler")

    mark = facebook_user.User()
    HHackers = mark.groups().filter(
        lambda g: "hack" in g.name.lower() or "hh" in g.name.lower())
        #lambda g: int(g.id) == 794333857297838)

    for group in HHackers:
        group_obj = group.persist()
        group_obj["last_updated"] = time.time()
        DAO.groups.save(group_obj)

        # save and log action
        current_group_id = group.id
        LOG.info("Persisted {} with id {} at time {}".format(
            group.name, group.id, datetime.datetime.now()
        ))
        for post in group.posts_(limit=300).take(300):
            post_obj = post.persist()
            post_obj["group_id"] = current_group_id
            # Define Context, id_ is to remove the GID_PID problem
            current_post_id = post.id_
            producer_id = post_obj["from_id"]
            # save and log action
            DAO.posts.save(post_obj)
            LOG.info("Persisted post with id {} at time {}".format(
                current_post_id, datetime.datetime.now()
            ))
            for comment in post.comments_(limit=300):
                comment_obj = comment.persist()
                comment_obj["group_id"] = current_group_id
                comment_obj["post_id"] = current_post_id
                # Define Context
                current_comment_id = comment_obj["id"]
                # save and log action
                DAO.comments.save(comment_obj)
                LOG.info("Persisted comment with id {} at time {}".format(
                    current_comment_id, datetime.datetime.now()
                ))
            for like in post.likes_(300):
                like_obj = like.persist()
                like_obj["group_id"] = current_group_id
                like_obj["post_id"] = current_post_id
                # save and log action
                DAO.likes.save(like_obj)
                LOG.info("Persisted post-like with id {} at time {}".format(
                    current_post_id, datetime.datetime.now()
                ))

    LOG.info("[JOB COMPLETED] {}".format(datetime.datetime.now()))
