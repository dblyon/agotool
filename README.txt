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

##############################################################################
##### tutorial / blog
### Docker
1. Bootstrap the DB
docker-compose up -d db
docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

2. Bring up the cluster
docker-compose up -d

3. Browse to localhost:8080 to see the app in action.

4. Take down the apps
docker-compose down
##############################################################################


psql -U postgres -d postgres -f ./copy_from_file_and_index_TEST.psql
tables_dir = r"/agotool_data/PostgreSQL/tables"
static_dir = r"/agotool_data/PostgreSQL/static"
##############################################################################
### Docker from DBL for agotool
0. write proper requirements.txt (NOT pip freeze > requirement.txt)
pipreqs --force .
1. build images from docker-compse.yml
docker-compose build
2. run images in background
docker-compose up -d
3. get the container id for the PostgreSQL DB
docker ps
4. run psql scripts to populate DB (from host run the psql script in the container)
# First time setup
docker exec -it agotool_db_1 psql -U postgres -d postgres -f /agotool_data/PostgreSQL/create_DBs.psql
# TESTING
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/PostgreSQL/copy_from_file_and_index_TEST.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/PostgreSQL/drop_and_rename.psql
# real DB/not testing
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/copy_from_file_and_index.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/drop_and_rename.psql

5. monthly UPDATES
docker exec -it agotool_flask_1 python ./python/update_manager.py
docker run --rm -it agotool_flask_1 python ./python/update_manager.py
# spin up another instance of agotool_flaskapp image as temporary container that is removed after the commands finish
docker run --rm -it --name secinstance --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py
docker run --rm -it --name secinstance --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash

##############################################################################
##### copy data to named volume
# spin up another container that deletes itself after it is done
docker run --rm -it --volume ~/modules/cpr/agotool/data:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash
# as soon as I exit the container will delete itself. Self destruction
# volume data persists

# alternative to 2 named volumes:
# 1 volume with 2 sources and 2 different mount points
##############################################################################
# scale a service like the flask-app
docker-compose up -d --scale flaskapp=2



Resources:
https://stackoverflow.com/questions/27735706/docker-add-vs-volume

docker exec -it 1769d6ea0667 psql -U postgres -d agotool_test "\dt"

docker-compose run --rm flaskapp /bin/bash -c "python /opt/services/flaskapp/src/python/update_manager.py"

### Tree structure of repo
.
├── app
│   ├── conf.d
│   ├── python
│   └── static
│       ├── css
│       ├── js
│       └── templates
└── data
    ├── Background_Reference_Proteomes
    ├── PostgreSQL
    │   ├── downloads
    │   ├── static
    │   └── tables
    │       └── test
    ├── exampledata
    ├── logs
    └── session

###############################################################################
### Fixing file stream issues for agotool
--> solution was fixing the jinja templating, specifically the URLs
for the files using flask serve_files_from_directory and the following
# processes should be "1", otherwise nginx throws 502 errors with large files
app.run(host='0.0.0.0', port=5911, processes=1, debug=variables.DEBUG)
###############################################################################

### fixing MCL clustering
docker run --rm -it --name secinstance --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash
mcl /agotool_data/data/session/mcl_in_91_1518002421.200194.txt -I 1 --abc -o /agotool_data/data/session/mcl_out_91_1518002421.200194.txt