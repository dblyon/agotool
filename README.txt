##############################################################################
### installation on red hat virtual server
# copy static data to server (can be deleted after copying it to named volume)
rsync -avr /Users/dblyon/modules/cpr/agotool/data david@10.34.6.24:/data_from_ody/
# pull github repo
git clone ...
or
cd /var/www/agotool
git pull origin docker
# change preload to False in /var/www/agotool/app/python/variables.py, PRELOAD = False
vim /var/www/agotool/app/python/variables.py
# build the images
docker-compose build
# copy data to named volume (spin up another container that deletes itself after it is done)
docker run --rm -it --volume /data_from_ody:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp rsync -avr /mounted_data/data /agotool_data/
# delete data if needed
rm -rf /data_from_ody
# download newest resources
docker run --rm -it --name update --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py
# test DB
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/copy_from_file_and_index_TEST.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/drop_and_rename.psql
# populate DB for real
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/copy_from_file_and_index.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/drop_and_rename.psql
# change "preload" to True, change "skip_slow_downloads" to False, change "debug" to False
vim /var/www/agotool/app/python/variables.py
--> tadaaa it should work now
### scale a service like the flask-app
docker-compose up -d --scale flaskapp=2
##############################################################################
##### Tree structure of local version of repo
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

##### on virtual server
# named volume
/agotool_data/
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

# and in /opt/services/flaskapp/src
.
├── conf.d
├── python
└── static
    ├── css
    ├── js
    └── templates
##############################################################################
##############################################################################
### Docker from DBL for agotool local (Ody)
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
docker exec -it agotool_db_1 psql -U postgres -d postgres -f /agotool_data/data/PostgreSQL/create_DBs.psql
docker exec -it agotool_db_1 --volume "agotool_agotool_data:/agotool_data" psql -U postgres -d postgres -f ./app/sql/create_DBs.psql
# TESTING
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f ./app/postgres/copy_from_file_and_index_TEST.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f ./app/postgres/drop_and_rename.psql
# real DB/not testing
docker exec -it agotool_db_1 psql -U postgres -d agotool -f ./app/postgres/copy_from_file_and_index.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool -f ./app/postgres/drop_and_rename.psql
# test DB
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /Users/dblyon/modules/cpr/agotool/data/PostgreSQL/copy_from_file_and_index_TEST_ODY.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /Users/dblyon/modules/cpr/agotool/data/PostgreSQL/drop_and_rename.psql
# populate DB for real
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /Users/dblyon/modules/cpr/agotool/data/PostgreSQL/copy_from_file_and_index_ODY.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /Users/dblyon/modules/cpr/agotool/data/PostgreSQL/drop_and_rename.psql
5. monthly UPDATES
# spin up another instance of agotool_flaskapp image as temporary container that is removed after the commands finish
docker run --rm -it --name update --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py
# check out the named volume
docker run --rm -it --name checkvolume --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash
# check out the Postgres DB
docker run --rm -it --name checkdb --volume "dbdata:/var/lib/postgresql/data" postgres bash
##############################################################################
##### copy data to named volume
# spin up another container that deletes itself after it is done
docker run --rm -it --volume /data_from_ody:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp rsync -avr /mounted_data/data /agotool_data/
docker run --rm -it --volume /agotool_data:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash

# as soon as I exit the container will delete itself. Self destruction
# volume data persists

# alternative to 2 named volumes:
# 1 volume with 2 sources and 2 different mount points
##############################################################################
##############################################################################
### Fixing file stream issues for agotool
--> solution was fixing the jinja templating, specifically the URLs
for the files using flask serve_files_from_directory and the following
# processes should be "1", otherwise nginx throws 502 errors with large files
app.run(host='0.0.0.0', port=5911, processes=1, debug=variables.DEBUG)
##############################################################################
# deprecated readme below
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
##### crontab on red hat virtual server
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

# added David Lyon
0 4 1 * * root /var/www/agotool/app/update_DB.sh >> /agotool_data/data/logs/updates_log.txt 2>&1 &
#30 *   * * *   dblyon  /home/dblyon/bin/restart_if_down.sh
##############################################################################
### restart if down, deprecated and needs debugging
#!/bin/bash
if ps aux | grep "python3 runserver.py" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
    mail -s "aGOtool is restarting" dblyon@gmail.com < /var/www/agotool/logs/update.log
    cd /var/www/agotool
    sudo -u agotool python3 runserver.py >> /var/www/agotool/logs/runserver.log 2>&1 &
fi
##############################################################################