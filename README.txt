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

### Docker
1. Bootstrap the DB
docker-compose up -d db
docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"
docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

2. Bring up the cluster
docker-compose up -d

3. Browse to localhost:8080 to see the app in action.

4. Take down the apps
docker-compose down
