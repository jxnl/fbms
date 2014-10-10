"""
marksweep.examples-facebook
~~~~~~~~~~~~~~~~~~

this modules provides some examples of how to use the facebook classes
"""

import user

MAX_PAGE_SIZE = 10
GET_ALL_POSTS = False


def list_of_groups(user):
    return list(user.groups(MAX_PAGE_SIZE))


def list_of_hh_groups(user):
    """You can use itertools to go through the content stream
    before saving it to a list"""
    return list(filter(
        lambda g: "hack" in g.name.lower() or "hh" in g.name.lower(),
        mark.groups(MAX_PAGE_SIZE)))


def get_posts_from_groups(user):
    """use dotted access as if your return objects are json"""
    groups = list_of_hh_groups(user)
    names = []
    for group in groups:
        # it knows to sleep incase it ever gets rate limited!
        for post in group.posts(5):
            names += [group.name + ":" + post.user.name]
    return names

if __name__ == "__main__":
    mark = user.User()
    """ printing directly puts it into json!
        if you want to persist! """
    for group in list_of_groups(mark):
        print group
    """ built with generators!
        memory efficient and lazy evaluated """
    for name in [g.name for g in list_of_hh_groups(mark)]:
        print name
    """ very expressive! """
    for keyvalue in get_posts_from_groups(mark):
        print keyvalue
