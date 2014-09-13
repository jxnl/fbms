import group_poller
import time

import datetime
from datetime import timedelta

access_token = "CAAK5npFF7MYBACPwdYQRuqHwmQj18YsRDdkUiU1WfyHvs2a5AaNzyNihyqXg18UdGTyaJi9pWReXGQmJZAMtDpvOM8jqQ6c1GuvQLdKqLjvTHhyBIsYU26iLcLgUZAj4e9hnV9iyZAjwi4tr2gk5TAcNNJ71Nyctmzro1GFaikZCfVaoB42BS6AtEY6ypFZAxf6wpGUSYAjD3TMusTUeA"
group_id = '369653806521044'

last_update_times = dict()

gp = group_poller.GroupPoller(access_token, group_id)

delay = timedelta(0, 1)
last_tick = datetime.datetime.utcnow()

while True:
    new_posts = gp.paginate_all(max_delta=delay)

    print len(new_posts)

    last_tick = datetime.datetime.utcnow()
    time.sleep(delay.seconds)
