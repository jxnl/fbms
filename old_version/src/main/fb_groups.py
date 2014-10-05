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

        print len(list(all_posts))

    def paginate_all(self):
        posts = self.graph.get_connections(self.group_id, "feed")
        all_posts = list()
        while True:
            try:
                for post in posts['data']:
                    all_posts.append(FacebookPost(post))
                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                break
        for i in all_posts:
            print(i.id_, i.message_)


class FacebookPost:
    def __init__(self, post):
        keys = ['id', 'from', 'message']

        for key in keys:
            setattr(self, key + '_', post[key])

gp = GroupPoller('CAACEdEose0cBAH200rymswkld6e3HHBmH5DoIfsM9ySTQIKixknJZBOUOZAHnaGIitAKKi0QviZBa33Ko7ajrfJnZBy9wZANWsG8VTzrtnEMUZCBWHePLcQy1aEPPwV9vA6fNeAYNaoaXheOeVwXjPRABoEUhU1oVHJcDyfzHuk2hAZAxO2KX42Qg45H2ia9N4w1PdZAOzfNkA04KYMFVkHlhKZB8O8dXrGAZD',
                 '2468059626')
gp.paginate_all()
