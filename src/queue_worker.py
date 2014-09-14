import queue_writer
import time

from Queue import Queue
from threading import Thread
from processing import Classifier

# Define the access tokens and group_ids
access_token = "CAAK5npFF7MYBACPwdYQRuqHwmQj18YsRDdkUiU1WfyHvs2a5AaNzyNihyqXg18UdGTyaJi9pWReXGQmJZAMtDpvOM8jqQ6c1GuvQLdKqLjvTHhyBIsYU26iLcLgUZAj4e9hnV9iyZAjwi4tr2gk5TAcNNJ71Nyctmzro1GFaikZCfVaoB42BS6AtEY6ypFZAxf6wpGUSYAjD3TMusTUeA"
group_id = '369653806521044'

print "\nStarting Mark Sweep (v0.1)"
print "Written by Jason Liu, Henry Boldizsar and Taylor Blau at PennApps X"
print "\n-----------------"

# Some constants, creates the queue and the workers
queue = Queue(maxsize=0)
num_workers = 8
write_interval = 0.75
clf = Classifier()


# Defines the action that will be taken on a given piece of data
def take_action(queue):
    while True:
        fb_entity = queue.get()
        # Do the shit - JSON HERE
        print "got a post! {}".format(fb_entity.contents)
        msg = fb_entity.content
        t = clf.process(msg)

        if t['spam'][1] > .95:
            fb_entity.delete_post(access_token)
        elif t['spam'] > 80 and not t['ontopic']:
            fb_entity.post_comment('This post has been mark suspecious',
                                   access_token)
        else:
            pass

        fb_entity.post_comment("Hello, you said: {}".format(fb_entity.contents),
                               access_token)
        queue.task_done()

# Spawn up the workers
for i in range(num_workers):
    print "Spawning up worker #{}".format(i + 1)
    worker = Thread(target=take_action, args=(queue,))
    worker.setDaemon(True)
    worker.start()

print "-----------------\n"

# Creates the queue writer
writer = queue_writer.QueueWriter(access_token, group_id)

# And finally, subscribe to the queue so that the program keeps running until everything is removed from the queue
print "Subscribing to the queue, ready to accept posts/comments...\n"
while True:
    try:
        writer.write(queue)
        queue.join()

        time.sleep(write_interval)
    except KeyboardInterrupt:
        print "Shutting down..."
        break
