# -*- coding: utf-8 -*-

"""
marksweep.group-crawler-dfs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This modules contains a crawler that will traverse the facebook graph depth-first and persist
all groups, posts, comments and likes.
"""

__author__ = 'JasonLiu'

from Queue import Queue
import logging
import datetime
import time

from pymongo import MongoClient

import facebook_user


class AbstractBaseCrawler(object):
    """AbstractBaseCrawler: contains the required access for writing FBObjects to MongoDB"""

    logging.basicConfig(
        filename="../logs/crawler.log",
        level=logging.DEBUG
    )

    def __init__(self, name="marksweep"):
        self.name = name
        self.user = facebook_user.User()
        # noinspection PyUnresolvedReferences
        self.groups = mark.groups(limit=1000).filter(
            lambda _: "hack" in _.name.lower() or "hh" in _.name.lower()
        )
        self.DAO = MongoClient().hackathonhackers
        self.LOG = logging.getLogger("bfs-crawler : {}".format(name))
        self.get_all_posts = False

    def get_all_posts(self):
        """
        If this is set, the crawler will go through all of the posts for each group instead of a single page

        :return:
        """
        self.get_all_posts = True
        return self

    def _crawl_group(self, group):
        """
        Take a group FBObject and persist to MongoDB

        :param group:
        :return:
        """
        group_obj = group.persist()
        group_obj["last_updated"] = time.time()
        self.DAO.groups.save(group_obj)
        # save and log action
        self.LOG.info("[GROUP-{}] (id={},time={})".format(
            group.name, group.id, datetime.datetime.now()
        ))

    def _crawl_group_post(self, post, current_group_id):
        """
        Take a post FBObject and persist to MongoDB

        :param post:
        :param current_group_id:
        :return:
        """
        post_obj = post.persist()
        post_obj["group_id"] = current_group_id
        # save and log action
        self.DAO.posts.save(post_obj)
        self.LOG.info("[GROUP-POST] (id={},time={})".format(
            post.id, datetime.datetime.now()
        ))

    def _crawl_post_comments(self, comment, group_id, post_id):
        """
        Take a post comment FBObject and persist to MongoDB

        :param comment:
        :param group_id:
        :param post_id:
        :return:
        """
        comment_obj = comment.persist()
        comment_obj["group_id"] = group_id
        comment_obj["post_id"] = post_id
        # Define Context
        current_comment_id = comment_obj["id"]
        # save and log action
        self.DAO.comments.save(comment_obj)
        # noinspection PyUnresolvedReferences
        self.OG.info("Persisted comment with id {} at time {}".format(
            current_comment_id, datetime.datetime.now()
        ))

    def _crawl_post_likes(self, like, group_id, post_id):
        """
        Take a post comment FBObject and persist it MongoDb

        :param like:
        :param group_id:
        :param post_id:
        :return:
        """
        like_obj = like.persist()
        like_obj["group_id"] = group_id
        like_obj["post_id"] = post_id
        # save and log action
        self.DAO.likes.save(like_obj)
        # noinspection PyUnresolvedReferences
        self.LOG.info("Persisted post-like with id {} at time {}".format(
            post_id, datetime.datetime.now()
        ))

    def crawl(self):
        raise NotImplementedError("What, why did you use the abstract base class?")


class GroupCrawlerDFS(AbstractBaseCrawler):
    def __init__(self, name="marksweep"):
        super(GroupCrawlerDFS, self).__init__(name)
        self.LOG = logging.getLogger("dfs-crawler : {}".format(name))

    def crawl(self, lim=100):
        """
        This crawl will traverse the Facebook graph depth first and persist all FBObjects

        :param lim: total number of posts to get per page.
        :return:
        """
        self.LOG.info("[JOB INITIATED] {}".format(datetime.datetime.now()))
        for group in self.groups:
            current_group_id = group.id
            self._crawl_group(group)
            for post in group.posts_(limit=lim, all=self.get_all_posts):
                current_post_id = post.id_
                self._crawl_group_post(post, current_group_id)
                for comment in post.comments_(limit=500, all=True):
                    self._crawl_post_comments(comment, current_group_id, current_post_id)
                for like in post.likes_(limit=500, all=True):
                    self._crawl_post_likes(like, current_group_id, current_post_id)
        self.LOG.info("[JOB COMPLETED] {}".format(datetime.datetime.now()))


class GroupCrawlerBFS(AbstractBaseCrawler):
    def __init__(self, name='marksweep'):
        super(GroupCrawlerBFS, self).__init__(name)
        self.group_queue = Queue()
        self.posts_queue = Queue()
        self.LOG = logging.getLogger("bfs-crawler : {}".format(name))

    def crawl(self, lim=100):
        """
        This crawl will traverse the Facebook graph breadth first with respect
        to posts and then and persist all FBObjects

        :param lim: total number of posts to get per page.
        :return:
        """
        self.LOG.info("[JOB INITIATED : QUEUING GROUP NODES] {}".format(datetime.datetime.now()))
        # Visit all groups and push into queue
        for group in self.groups:
            self.group_queue.put(group)

        self.LOG.info("[VISITING GROUP NODES] {}".format(datetime.datetime.now()))
        # For each group get the first 100 posts
        # Push each post onto the queue
        while not self.group_queue.empty():
            for group in self.group_queue.get():
                self.LOG.info("[QUEUEING POST NODES] {}".format(datetime.datetime.now()))
                for post in group.posts_(limit=lim, all=self.get_all_posts):
                    self.posts_queue.put(post)

        self.LOG.info("[VISITING POST NODES] {}".format(datetime.datetime.now()))
        # For each post from the queue
        # Persist all comments and likes
        while not self.posts_queue.empty():
            for post in self.posts_queue.get():
                current_post_id = int(post.id_)
                current_group_id = int(post.group_id_)
                self._crawl_group_post(post, current_group_id)
                # Comments and Likes are crawled depth first
                self.LOG.info("[VISITING COMMENT NODES] {}".format(datetime.datetime.now()))
                for comment in post.comments_(limit=500, all=True):
                    self._crawl_post_comments(comment, current_group_id, current_post_id)
                self.LOG.info("[VISITING LIKE NODES] {}".format(datetime.datetime.now()))
                for like in post.likes_(limit=500, all=True):
                    self._crawl_post_likes(like, current_group_id, current_post_id)
        self.LOG.info("[JOB COMPLETED] {}".format(datetime.datetime.now()))
