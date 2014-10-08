from config import ACCESS_TOKEN
from utils import trim
import facebook


class Group(object):
    def __init__(self, group_data_object):
        for k in group_data_object:
            self.__setattr__(str(k), str(group_data_object[k]))

    def __repr__(self):
        return self.id


class User(object):
    def __init__(self):
        self.graph = facebook.GraphAPI(ACCESS_TOKEN)

    def groups(self, limit=5, get_all=False):
        response = self.graph.get_connections("me", "groups", limit=limit)
        groups = [Group(g) for g in response["data"]]
        for grp in groups:
            yield grp
            if response["data"]:
                next_page = trim(response["paging"]["next"])
                response = self.graph.request(next_page)
                groups += [Group(g) for g in response["data"]]

if __name__ == "__main__":
    mark = User()
    for group in mark.groups():
        print group.name
        print group
