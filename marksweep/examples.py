"""
marksweep.examples-facebook
~~~~~~~~~~~~~~~~~~

this modules provides some examples of how to use the facebook classes
"""

import user

if __name__ == "__main__":
    # Create the user
    mark = user.User()
    """ printing directly puts it into json!
        if you want to persist! """
    # take 10 groups from HH
    HHgroups = mark.groups().filter(
        lambda g: "hack" in g.name.lower() or "hh" in g.name.lower()).take(10)

    for group in HHgroups:
        print group
        for post in group.posts().take(10):
            print post
            for comments in post.comments().take(10):
                print comments
