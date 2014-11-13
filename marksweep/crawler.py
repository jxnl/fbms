"""
marksweep.crawler
~~~~~~~~~~~~~~~~~~

"""

import user
import logging
import datetime
from pymongo import MongoClient

logging.basicConfig(filename="../logs/crawler.log",
                    level=logging.DEBUG)

if __name__ == "__main__":
    DAO = MongoClient().hackathonhackers
    LOG = logging.getLogger("crawler")

    mark = user.User()
    HHDataHackers = mark.groups().filter(
        #lambda g: "hack" in g.name.lower() or "hh" in g.name.lower())
        lambda g: "data hackers" in g.name.lower())

    for group in HHDataHackers:
        group_obj = group.persist()
        DAO.groups.save(group_obj)

        # save and log action
        current_group_id = group_obj["id"]
        LOG.info("Persisted {} with id {} at time {}".format(
            group.name, group.id, datetime.datetime.now()
        ))
        for post in group._posts(limit=300):
            post_obj = post.persist()
            post_obj["group_id"] = current_group_id
            # Define Context
            current_post_id = post_obj["id"]
            producer_id = post_obj["from_id"]
            # save and log action
            DAO.posts.save(post_obj)
            LOG.info("Persisted post with id {} at time {}".format(
                current_post_id, datetime.datetime.now()
            ))
            for comment in post._comments():
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
                for clike in comment._likes():
                    clike_obj = clike.persist()
                    clike_obj["group_id"] = current_group_id
                    clike_obj["post_id"] = current_post_id
                    clike_obj["comment_id"] = current_comment_id
                    # save and log action
                    DAO.likes.save(clike_obj)
                    LOG.info("Persisted comment-like with id {} at time {}".format(
                        current_comment_id, datetime.datetime.now()
                    ))
            for like in post._likes():
                like_obj = like.persist()
                like_obj["group_id"] = current_group_id
                like_obj["post_id"] = current_post_id
                # save and log action
                DAO.likes.save(like_obj)
                LOG.info("Persisted post-like with id {} at time {}".format(
                    current_post_id, datetime.datetime.now()
                ))

    LOG.info("[JOB COMPLETED] {}".format(datetime.datetime.now()))
