import facebook
import requests

access_token = "CAACEdEose0cBAGGNZAexdC5rzU85TgFwxkKTYV5zPkYHEU82CRZANUcdEeu2RB7qCF44DKAZB8X1sfkO4lYvVfF1ixXL5NuWEg8yGpvYCAEbK2gjLn8M9ZByU9iYVPwl2e1rnithXrNTKxYiVRT6QsjyVZCWUzyKZAstqzVEyMBZC1hzzr5c62Vl2TZBfqDx4MS82Yk0fkkfeVaBrkXxhE7Q"

class GroupPoller:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)

    def paginate_top(self):
        posts = self.graph.get_connections(self.group_id, "feed")
        all_posts = (FacebookPost(post) for post in posts['data'])

        print len(list(all_posts))

class FacebookPost:
    def __init__(self, post):
        keys = ['id', 'from', 'message']

        for key in keys:
            setattr(self, key + '_', post[key])
    def post_comment (body, post_id)
        r = requests.post('https://graph.facebook.com/v2.1/' + post_id + '/comments?access_token=' + access_token + '&message=' + body)
        r.json()

gp = GroupPoller('CAACEdEose0cBAGGNZAexdC5rzU85TgFwxkKTYV5zPkYHEU82CRZANUcdEeu2RB7qCF44DKAZB8X1sfkO4lYvVfF1ixXL5NuWEg8yGpvYCAEbK2gjLn8M9ZByU9iYVPwl2e1rnithXrNTKxYiVRT6QsjyVZCWUzyKZAstqzVEyMBZC1hzzr5c62Vl2TZBfqDx4MS82Yk0fkkfeVaBrkXxhE7Q', '298947700283856')
gp.paginate_top()
