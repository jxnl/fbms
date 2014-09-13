import group_poller

import csv
import codecs

# should last 60+ days.. call this to extend https://graph.facebook.com/oauth/access_token?client_id=767040646671558&client_secret=4c20235c2033d68a5bc6c52895c987f3&grant_type=fb_exchange_token&fb_exchange_token=CAAK5npFF7MYBAHgIpe1fVMrwXdhpfh7eA9SkLoPsGcZBsa9BYASJDH7ARTAtiVV2I5PrXHOfwuqiZAKK2HXYWRF5U546Ux4LeifPE4OfZBjZCv1aNr03wP99otRROleqzGvSWurCYhefmtMTjn5PTViDJCWp0J6JLhOi3SYTtt5eeULjtHJMyUprPPa0KJugqLnrcXHqEEYAIiWqYIz7OTreMMB38JUZD

access_token = "CAAK5npFF7MYBACPwdYQRuqHwmQj18YsRDdkUiU1WfyHvs2a5AaNzyNihyqXg18UdGTyaJi9pWReXGQmJZAMtDpvOM8jqQ6c1GuvQLdKqLjvTHhyBIsYU26iLcLgUZAj4e9hnV9iyZAjwi4tr2gk5TAcNNJ71Nyctmzro1GFaikZCfVaoB42BS6AtEY6ypFZAxf6wpGUSYAjD3TMusTUeA"

gp = group_poller.GroupPoller(access_token, '759985267390294')
all_posts = gp.paginate_all(100)

with open('hh.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")

    for post in all_posts:
        writer.writerow([1, post.contents.encode('utf-8')])
