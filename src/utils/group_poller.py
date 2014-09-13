import facebook
import requests

access_token = "CAACEdEose0cBAK06LI4q47krSNnrous4jgIbV15eEXKdLgMiEjrnsG1lzb9wG5U8bKYJk8GS4F0O7RJ8goPQ570fWZC709qrj32jHXFl0PrBJVi2ZByZB0WVdI3W658BeLzw3CJl9SQ9gAu6ycW2NCQuimh16V5PRmcc8YkZAvOaNlrMZAwODBV1y89hEo8JxPfB37vUA2hMkfXRD7sOq"

class GroupPoller:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)

    def paginate_top(self):
        posts = self.graph.get_connections(self.group_id, "feed")
        all_posts = (FacebookPost(post) for post in posts['data'])

        for post in all_posts:
            print post.post_id + "||" + post.contents.replace("\n", " ")

    def paginate_all(self):
        posts = self.graph.get_connections(self.group_id, "feed")

        while True:
            try:
                for post in posts['data']:
                    FacebookPost(post)

                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                break

class FacebookPost:
    def __init__(self, post):
        self.group_id = post['id'].split("_")[0]
        self.post_id = post['id'].split("_")[1]

        self.poster = post['from']
        self.contents = post['message']
        
    def post_comment(self, body, post_id):
        r = requests.post('https://graph.facebook.com/v2.1/' + post_id + '/comments?access_token=' + access_token + '&message=' + body)
        return r.json()

gp = GroupPoller(access_token, '298947700283856')
gp.paginate_top()
