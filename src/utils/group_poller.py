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
            print post.post_id + "||" + post.contents.replace("\n", " ")

    def paginate_all(self, max_results=100):
        all_posts = list()
        posts = self.graph.get_connections(self.group_id, "feed")

        while True:
            # This will evaluate to false when there is no data
            if 'paging' in posts:
                for post in posts['data']:
                    fb_post = FacebookPost(post)
                    if fb_post:
                        # Stop returning an infinite result after the max_results is reached
                        if len(all_posts) > max_results - 1:
                            return all_posts
                        else:
                            all_posts.append(fb_post)

                posts = requests.get(posts['paging']['next']).json()
            else:
                break

        return all_posts

class FacebookPost:
    def __init__(self, post):
        self.group_id = post['id'].split("_")[0]
        self.post_id = post['id'].split("_")[1]

        self.poster = post['from']

        # Not all posts have messages, apparently!
        try:
            self.contents = post['message']
        except KeyError:
            return # It'll just return nil if nothing exists

        self.comments = list()

        # Some posts also don't have any comments
        if 'comments' in post:
            for comment in post['comments']['data']:
                self.comments.append(FacebookComment(self, comment))

    def post_comment(self, body, post_id):
        r = requests.post('https://graph.facebook.com/v2.1/' + post_id + '/comments?access_token=' + access_token + '&message=' + body)
        return r.json()

class FacebookComment:
    def __init__(self, parent_post, comment_raw):
        self.parent_post = parent_post

        self.poster = comment_raw['from']
        self.contents = comment_raw['message']
        self.like_count = comment_raw['like_count']
