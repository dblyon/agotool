command = "/mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/gunicorn" # location of python executable
timeout = 840 # seconds --> 14min (should take ~ 6-7 min on Atlas)
workers = 3 # number of python-flask workers
bind = "0.0.0.0:10111" # IP:Port
max_requests = 5000 # after 1000 requests to a particular worker plus randint(0, max_requests_jitter) offset, the worker is killed and another re-spawned
min_requests_jitter = 10000
max_requests_jitter = 50000
keep_alive = 30