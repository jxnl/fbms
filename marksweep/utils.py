# -*- coding: utf-8 -*-

"""
marksweep.utils
~~~~~~~~~~~~~~~~~~~~~

this module contains functions that help our code stay DRY and simple
"""

import user

def lazygen(holder, source, edges, limit=100, get_all=False):
    """lazy way to page through the content of an endpoint with a generator

    parameters:
    ~~~~~~~~~~
        graph (GraphAPI) - facbeook connection object
        holder (FBObject) - class that wraps the content dictionary
        source (str) - source node on facebook graph
        edge (str) - edge label on facebook graph
        limit (int) - max number of posts per page
        get_all (boolean) - if true, gets all posts from an endoint
    """
    graph = user.User.graph()
    response = graph.get_connections(source, edges, limit=limit)
    items = (holder(item) for item in response["data"])
    for item in items:
        yield item
        # Lazily go to next page if required
        if get_all and response["data"]:
            next_page = trim(response["paging"]["next"])
            response = graph.request(next_page)
            items += (holder(item) for items in response["data"])


def trim(paging_url):
    """trims the paging url to the uri"""
    return paging_url[26:]
