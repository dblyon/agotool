To run the server locally follow these steps:

1. clone repository from https://github.com/dblyon/agotool.git
2. execute 'static/python/update_server.py' to retrieve dependencies, which will be downloaded to 'static/data'
3. change the last line of code in 'runserver.py'
from:
app.run('0.0.0.0', 5911, processes=4, debug=False)
to:
app.run('localhost', 5000, processes=4, debug=False) # or something similar
4. execute 'runserver.py'
5. interact with the servers through your browser of choice at
http://127.0.0.1:5000/
6. have fun
7. cite us
8. take a break
