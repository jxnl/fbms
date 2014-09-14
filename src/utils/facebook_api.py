import dateutil.parser
import requests

class FacebookPost:
    def __init__(self, post):
        self.created_at = dateutil.parser.parse(post['created_time']).replace(tzinfo=None)

        self.group_id = post['id'].split("_")[0]
        self.post_id = post['id'].split("_")[1]

        self.poster = post['from']

        # Not all posts have messages, apparently!
        try:
            self.contents = post['message']
        except KeyError:
            self.contents = ""

        self.comments = list()

        # Some posts also don't have any comments
        if 'comments' in post:
            for comment in post['comments']['data']:
                self.comments.append(FacebookComment(self, comment))

    def post_comment(self, body, access_token):
        r = requests.post('https://graph.facebook.com/v2.1/' + self.post_id + '/comments?access_token=' + access_token + '&message=' + body)
        return r.json()

    def delete_post(self, access_token):
        r = requests.delete('https://graph.facebook.com/v2.1/' + self.post_id + '?access_token=' + access_token)
        return r.json()

class FacebookComment:
    def __init__(self, parent_post, comment_raw):
        self.parent_post = parent_post

        self.poster = comment_raw['from']
        self.contents = comment_raw['message']
        self.like_count = comment_raw['like_count']

    def post_comment(self, body):
        self.parent_post.post_comment(body)
