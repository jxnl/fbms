import group_poller

import csv
import codecs

access_token = "CAACEdEose0cBAOKcwPISS7FEOlEe5qZBJFVOT9rTKlf0RYFYeFX0NputJJt3AeztZAOX1N4pOQ64DriyLiZAtVB4JZA3HjC6BxzY6ZAHSDyykhur2isg5k4aMXZAQfkISYnN78ZBcSu9KdBUEIvOaoA1VicYCSjalFXsL2t1jAmMrTZAkSJV11BOqgELbH38QL1ZAqZBf1xQrn3amQ6IEkwxqX"

gp = group_poller.GroupPoller(access_token, '759985267390294')
all_posts = gp.paginate_all(100)

with open('hh.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, delimiter=",")

    for post in all_posts:
        writer.writerow([1, post.contents.encode('utf-8')])
