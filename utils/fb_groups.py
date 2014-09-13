import facebook
import requests

class GroupPoller:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)

    def paginate_top(self):
        posts = self.graph.get_connections(self.group_id, "feed")
        all_posts = (FacebookPost(post) for post in posts['data'])

        for post in all_posts:
            print post.id_ + " (" + post.from_['name'] + ")\n" + post.message_
            print "______________________________________"

class FacebookPost:
    def __init__(self, post):
        keys = ['id', 'from', 'message']

        for key in keys:
            setattr(self, key + '_', post[key])

gp = GroupPoller('CAACEdEose0cBAK06LI4q47krSNnrous4jgIbV15eEXKdLgMiEjrnsG1lzb9wG5U8bKYJk8GS4F0O7RJ8goPQ570fWZC709qrj32jHXFl0PrBJVi2ZByZB0WVdI3W658BeLzw3CJl9SQ9gAu6ycW2NCQuimh16V5PRmcc8YkZAvOaNlrMZAwODBV1y89hEo8JxPfB37vUA2hMkfXRD7sOq', '298947700283856')
gp.paginate_top()
