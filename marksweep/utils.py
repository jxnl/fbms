# -*- coding: utf-8 -*-

"""
marksweep.utils
~~~~~~~~~~~~~~~

this module contains functions that help our code stay DRY.

contents:
    lazygen - consumes Facebook Graph properties and returns generators
    that contains the desired nodes or edges. The generator also handles
    pagination when required.
"""

__author__ = 'JasonLiu'

import facebook_user
from lazyiter import Iter


def lazygen(holder, source, edges, limit, get_all):
    """
    Lazy generator that abstracts the pagination of GraphAPI responses.

    :param edges: str - edge label on facebook graph
    :param source: str - source label on facebook graph
    :param holder: FBObject - class that wraps the resulting node dict
    :param limit: int - maximum number of objects per page
    :param get_all: bool - paginate through everything if needed
    :return: generator of containing elements of type `holder`
    """
    return Iter(_lazygen(holder, source, edges, limit, get_all))


def _lazygen(holder, source, edges, limit=100, get_all=False):
    graph = facebook_user.User.graph()
    response = graph.get_connections(source, edges, limit=limit)
    items = (holder(item) for item in response["data"])
    for item in items:
        yield item
        # Lazily go to next page if required
        if get_all and response["data"]:
            try:
                next_page = trim(response["paging"]["next"])
                response = graph.request(next_page)
                items = (holder(item) for items in response["data"])
            except KeyError:
                pass


def trim(paging_url):
    """trims the paging url to the uri"""
    return paging_url[26:]
