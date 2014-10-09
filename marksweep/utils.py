# -*- coding: utf-8 -*-

"""
marksweep.utils
~~~~~~~~~~~~~~~~~~~~~

this module contains classes and functions that help in the development
of the marksweet software
"""

import facebook
from config import ACCESS_TOKEN

graph = facebook.GraphAPI(ACCESS_TOKEN)


def trim(paging_url):
    """trims the paging url to the uri"""
    return paging_url[26:]


def lazygen(holder, source, edges, limit=100, get_all=False):
    """lazy way to page through the content of an endpoint with a generator

    parameters:
    ~~~~~~~~~~
        holder (DocAccess) - Class that wraps the content dictionary
        source (str) - source node on facebook graph
        edge (str) - edge lable on facebook graph
        limit (int) - max number of posts per page
        get_all (boolean) - if true, gets all posts from an endoint
    """
    response = graph.get_connections(source, edges, limit=limit)
    items = (holder(item) for item in response["data"])
    for item in items:
        yield item
        # Lazily go to next page if required
        if get_all and response["data"]:
            next_page = trim(response["paging"]["next"])
            response = graph.request(next_page)
            items += (holder(item) for items in response["data"])


class DotAccess(dict):
    """light wrapper over the dictionary, allows for dotted access for
    top level values"""

    def __init__(self, group_data_object):
        dict.__init__(self, group_data_object)

    def __getattr__(self, attr):
        return self[attr]
