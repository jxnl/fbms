import facebook
import requests

class GroupPoller:
    def __init__(self, access_token, group_id):
        self.access_token = str(access_token)
        self.group_id = str(group_id)

        self.graph = facebook.GraphAPI(self.access_token)

    def paginate_all(self):
        posts = self.graph.get_connections(self.group_id, "feed")

        while True:
            try:
                for post in posts['data']:
                    FacebookPost(post).doink()

                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                break

class FacebookPost:
    def __init__(self, post):
        keys = ['id', 'from', 'message']

        for key in keys:
            setattr(self, key + '_', post[key])

    def doink(self):
        print self.id_ + '     ' + self.message_


gp = GroupPoller('CAACEdEose0cBAGGNZAexdC5rzU85TgFwxkKTYV5zPkYHEU82CRZANUcdEeu2RB7qCF44DKAZB8X1sfkO4lYvVfF1ixXL5NuWEg8yGpvYCAEbK2gjLn8M9ZByU9iYVPwl2e1rnithXrNTKxYiVRT6QsjyVZCWUzyKZAstqzVEyMBZC1hzzr5c62Vl2TZBfqDx4MS82Yk0fkkfeVaBrkXxhE7Q', '298947700283856')
gp.paginate_all()
