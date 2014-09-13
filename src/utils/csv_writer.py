import group_poller

import csv
import codecs

access_token = "CAACEdEose0cBAFiZAfzNsBS5IRXX4ZBHrGEmYmrNnlrD8LsE4qCN7GGR5pw6SkCeufx9hR72EP5UBTPlAuyN1ec22Xzee5kWEHdYR1CtALxluBs2KfCheY3LNIZCMzVCLFvhNpCm5gDHnZAhNxHp4hcmrARfcFVSAsBlar1rjRZChackZCD2nj8rhUnUpII0eKfncbnMcnC8rYcR8KBF3M"

gp = group_poller.GroupPoller(access_token, '759985267390294')
all_posts = gp.paginate_all(100)

with open('hh.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")

    for post in all_posts:
        writer.writerow([1, post.contents.encode('utf-8')])
