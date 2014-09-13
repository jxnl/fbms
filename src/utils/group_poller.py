import facebook
import requests

# should last 60+ days.. call this to extend https://graph.facebook.com/oauth/access_token?client_id=767040646671558&client_secret=4c20235c2033d68a5bc6c52895c987f3&grant_type=fb_exchange_token&fb_exchange_token=CAAK5npFF7MYBAHgIpe1fVMrwXdhpfh7eA9SkLoPsGcZBsa9BYASJDH7ARTAtiVV2I5PrXHOfwuqiZAKK2HXYWRF5U546Ux4LeifPE4OfZBjZCv1aNr03wP99otRROleqzGvSWurCYhefmtMTjn5PTViDJCWp0J6JLhOi3SYTtt5eeULjtHJMyUprPPa0KJugqLnrcXHqEEYAIiWqYIz7OTreMMB38JUZD

access_token = "CAAK5npFF7MYBACPwdYQRuqHwmQj18YsRDdkUiU1WfyHvs2a5AaNzyNihyqXg18UdGTyaJi9pWReXGQmJZAMtDpvOM8jqQ6c1GuvQLdKqLjvTHhyBIsYU26iLcLgUZAj4e9hnV9iyZAjwi4tr2gk5TAcNNJ71Nyctmzro1GFaikZCfVaoB42BS6AtEY6ypFZAxf6wpGUSYAjD3TMusTUeA"

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

class FacebookPost:
    def __init__(self, post):
        self.group_id = post['id'].split("_")[0]
        self.post_id = post['id'].split("_")[1]

        self.poster = post['from']
        self.contents = post['message']
        
    def post_comment(body, post_id):
        r = requests.post('https://graph.facebook.com/v2.1/' + post_id + '/comments?access_token=' + access_token + '&message=' + body)
        r.json()

gp = GroupPoller(access_token, '298947700283856')
gp.paginate_top()