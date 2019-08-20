##############################################################################
### push to dockerhub
export DOCKER_ID_USER="dblyon"
docker login
docker tag agotool dblyon/agotool
docker push dblyon/agotool
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
#### backup and restore docker named volume
# backup
docker run --rm \
  --volume [DOCKER_COMPOSE_PREFIX]_[VOLUME_NAME]:/[TEMPORARY_DIRECTORY_TO_STORE_VOLUME_DATA] \
  --volume $(pwd):/[TEMPORARY_DIRECTORY_TO_STORE_BACKUP_FILE] \
  ubuntu \
  tar cvf /[TEMPORARY_DIRECTORY_TO_STORE_BACKUP_FILE]/[BACKUP_FILENAME].tar /[TEMPORARY_DIRECTORY_TO_STORE_VOLUME_DATA]
# e.g.
docker run --rm --volume agotool_agotool_data:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar cvf /bind_mount_dir/named_volume_agotool_data_backup_20180209.tar /named_volume_dir



docker run --rm --volume agotool_dbdata:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar cvf /bind_mount_dir/named_volume_dbdata_backup_20180209.tar /named_volume_dir
# restore
docker run --rm \
  --volume [DOCKER_COMPOSE_PREFIX]_[VOLUME_NAME]:/[TEMPORARY_DIRECTORY_STORING_EXTRACTED_BACKUP] \
  --volume $(pwd):/[TEMPORARY_DIRECTORY_TO_STORE_BACKUP_FILE] \
  ubuntu \
  tar xvf /[TEMPORARY_DIRECTORY_TO_STORE_BACKUP_FILE]/[BACKUP_FILENAME].tar -C /[TEMPORARY_DIRECTORY_STORING_EXTRACTED_BACKUP] --strip 1
# e.g.
docker run --rm --volume agotool_agotool_data:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar xvf /bind_mount_dir/named_volume_agotool_data_backup_20180209.tar -C /named_volume_dir --strip 1
docker run --rm --volume agotool_dbdata:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar xvf /bind_mount_dir/named_volume_dbdata_backup_20180209.tar -C /named_volume_dir --strip 1

##### beta version on aquarius
### backup
docker run --rm --volume agotool_agotool_data:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar cvf /bind_mount_dir/named_volume_agotool_data_backup_20180903.tar /named_volume_dir
docker run --rm --volume agotool_dbdata:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar cvf /bind_mount_dir/named_volume_dbdata_backup_20180903.tar /named_volume_dir

### copy files
rsync -avv -e 'ssh -p 22222' /Users/dblyon/modules/cpr/agotool/named_volume_agotool_data_backup_20180903.tar dblyon@aquarius.meringlab.org://home/dblyon/agotool/data/named_volume_dbdata_backup_20180903.tar
rsync -avv -e 'ssh -p 22222' ./named_volume_dbdata_backup_20180903.tar dblyon@aquarius.meringlab.org://home/dblyon/agotool/data/named_volume_dbdata_backup_20180903.tar

### restore on aquarius
docker run --rm --volume agotool_agotool_data:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar xvf /bind_mount_dir/named_volume_agotool_data_backup_20180903.tar -C /named_volume_dir --strip 1
docker run --rm --volume agotool_dbdata:/named_volume_dir --volume $(pwd):/bind_mount_dir ubuntu tar xvf /bind_mount_dir/named_volume_dbdata_backup_20180903.tar -C /named_volume_dir --strip 1




##############################################################################
### tag and push flaskapp to dockerhub/docker cloud
docker tag 3d5c5b99296e dblyon/agotool_flaskapp
docker push dblyon/agotool_flaskapp
##############################################################################
# ToDo
# - push to dockerhub --> done
# - set branch docker to master --> done
# - create webhooks a la Lars (see below)
        git commit and push
        --> github/bitbucket notifies Dockerhub
        --> Dockerhub builds image
        --> missing piece: server pulls image and starts it up
# Drone IO (Milan is using on this)

# Lars automatic updates/webhooks
bitbucket/github
    webhooks on C++ repo
Dockerhub
    build settings
        trigger URL
paste webhook m dockerhub to bitbucket
##############################################################################
### asking Tim to change email address
docker run --rm -it --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash
##############################################################################
###### @ UZH IMLS
# change preload to False in ../app/python/variables.py, PRELOAD = False
otherwise flask needs access to Postgres which isn't populated yet

# build the images
docker-compose build

# pushed to image to dockerhub
export DOCKER_ID_USER="dblyon"
docker login
docker push dblyon/python_agotool

# commented out the "build" line in order to pull from dockerhub next time instead of building from Dockerfile
  flaskapp:
  # build: . # uncomment to build from Dockerfile, else pull from dockerhub
    image: dblyon/python_agotool:latest

# start the containers
docker-compose up -d

# tmux and download newest resources and create DB files for import
docker run --rm -it --name update --user 5009:5009 --volume /mnt/mnemo5/dblyon/agotool:/agotool_data dblyon/python_agotool python ./app/python/update_manager.py


# test DB
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/copy_from_file_and_index_TEST.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/drop_and_rename.psql
# populate DB for real
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/copy_from_file_and_index.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/drop_and_rename.psql
# change "preload" to True, change "skip_slow_downloads" to False, change "debug" to False

##############################################################################
# really executed above
# scratch below


# copy data to named volume (spin up another container that deletes itself after it is done)
docker run --rm -it --volume /mnt/mnemo5/dblyon/agotool/data:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp rsync -avr /mounted_data /agotool_data/
# download newest resources
docker run --rm -it --name update --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py
# run containers and create "dbdata" volume
docker-compose up -d

# change preload to False in ../app/python/variables.py, PRELOAD = False
vim /var/www/agotool/app/python/variables.py

docker run --rm -it --name work --volume /mnt/mnemo5/dblyon/agotool/data:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash

### up next
# test DB
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/copy_from_file_and_index_TEST.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/drop_and_rename.psql


docker run --rm -it --name test --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp bash

#### DEBUG
# change docker default location to store files
# check disk usage of default storage loaction
sudo du -sh /var/lib/docker
788K	/var/lib/docker

#### How to store data
# Postgres data in named volume "dbdata"
- "dbdata:/var/lib/postgresql/data"
# Otherwise might be a better solution to not have another named volume like at CPR/SUND
# but a bind mount
- /mnt/mnemo5/dblyon/agotool/data:/agotool_data


docker run --rm -it --name test --volume /mnt/mnemo5/dblyon/agotool:/agotool_data centos bash
docker exec -it bash

### RSYNC between Ody and Atlas
rsync -av --exclude .git /Users/dblyon/modules/cpr/agotool/ dblyon@imlslnx-atlas.uzh.ch:/mnt/mnemo5/dblyon/agotool
rsync -av --exclude .git dblyon@imlslnx-atlas.uzh.ch:/mnt/mnemo5/dblyon/agotool/ /Users/dblyon/modules/cpr/agotool

##########################################################################################
### Tim at SUND to change email address
# log into virtual server

# change files locally at
# There are 2 files which would have to be edited:
vim /var/www/agotool/app/static/templates/FAQ.html (1x at the bottom)
vim /var/www/agotool/app/static/templates/about.html (2x at the top and in the middle)

# stop the docker containers
docker-compose down

# build the images again, which should incorporate the local changes
docker-compose build

# start the docker containers again
docker-compose up -d --scale flaskapp=2

# check that things are running correctly, this should list 4 containers (2x flaskapp, 1x postgres, 1x nginx)
docker ps
##########################################################################################


docker run --rm -it --name test --user 5009:5009 --volume /mnt/mnemo5/dblyon/agotool:/agotool_data dblyon/python_agotool bash
docker exec -it agotool_flaskapp_1 bash

##########################################################################################
### @ Ody, local version
### file structure locally, dblyon@Ody ...modules/cpr/agotool restapi
$ tree -d
.
├── app
│   ├── conf.d
│   ├── python
│   │   └── __pycache__
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

# set "PRELOAD = False"
vim /app/python/variables.py

# build the images
docker-compose build

# run containers
docker-compose up -d

# copy data to named volume (spin up another container that deletes itself after it is done)
docker run --rm -it --volume /Users/dblyon/modules/cpr/agotool:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp rsync -avr /mounted_data/data /agotool_data/

# delete data if needed, skipped (for later to save disk space)
rm -rf /Users/dblyon/modules/cpr/agotool/data

# download newest resources, skipped
docker run --rm -it --name update --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py

# test DB
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/copy_from_file_and_index_TEST.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool_test -f /agotool_data/data/PostgreSQL/drop_and_rename.psql

# populate DB for real
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/copy_from_file_and_index.psql
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/drop_and_rename.psql

# change "preload" to True
# change "debug" to False
vim /var/www/agotool/app/python/variables.py

# run the app with new settings
docker-compose up -d

##### Pytest run tests in test_userinput.py
# test works but flask crashes "error code 247", restart flask with docker-compose up -d
docker exec -it agotool_flaskapp_1 pytest -v ./python/test_userinput.py
--> /opt/services/flaskapp/src/env_file
## connect container to network
docker run --rm -it --network="agotool_db_nw" --name testing --volume "agotool_agotool_data:/agotool_data" --volume "agotool_dbdata:/dbdata" agotool_flaskapp bash
# check DB connection
cd app/python
python
import query
c = query.get_cursor_docker(host="db", dbname="agotool", user="postgres", password="USE_YOUR_PASSWORD", port="5432")
# pass environmental variables at container creation
docker run --rm -it --network="agotool_db_nw" --name testing -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="USE_YOUR_PASSWORD" -e POSTGRES_DB="agotool" -e APP_SECRET_KEY="USE_YOUR_SECRET_KEY" --volume "agotool_agotool_data:/agotool_data" --volume "agotool_dbdata:/dbdata" agotool bash
# ImportMismatchError from pytest
docker run --rm -it --network="agotool_db_nw" --name testing -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="USE_YOUR_PASSWORD" -e POSTGRES_DB="agotool" -e APP_SECRET_KEY="USE_YOUR_SECRET_KEY" --volume "agotool_agotool_data:/agotool_data" --volume "agotool_dbdata:/dbdata" agotool pytest -v ./app/python/test_userinput.py
--> /opt/services/flaskapp/src/app/env_file
docker run --rm -it --network="agotool_db_nw" --name testing -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="USE_YOUR_PASSWORD" -e POSTGRES_DB="agotool" -e APP_SECRET_KEY="USE_YOUR_SECRET_KEY" --volume "agotool_agotool_data:/agotool_data" --volume "agotool_dbdata:/dbdata" agotool bash

### connect to PostgreSQL container from host
psql --host localhost -U postgres -d agotool


### error 247
docker-compose up
--> 3 containers running
docker exec -it agotool_flaskapp_1 pytest -v ./python/test_userinput.py
--> works but error/crash "agotool_flaskapp_1 exited with code 247"
docker-compose up -d
--> restart flaskapp
docker run --rm -it --network="agotool_db_nw" --name testing -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="USE_YOUR_PASSWORD" -e POSTGRES_DB="agotool" -e APP_SECRET_KEY="USE_YOUR_SECRET_KEY" --volume "agotool_agotool_data:/agotool_data" --volume "agotool_dbdata:/dbdata" agotool pytest -v ./app/python/test_userinput.py
--> py._path.local.LocalPath.ImportMismatchError: ('conftest', '/opt/services/flaskapp/src/python/conftest.py', local('/opt/services/flaskapp/src/app/python/conftest.py'))
    ERROR: could not load /opt/services/flaskapp/src/app/python/conftest.py
Why is there a dicrepancy in the path:
docker exec -it agotool_flaskapp_1 bash
--> /opt/services/flaskapp/src/python/test_userinput.py
vs
docker run --rm -it --network="agotool_db_nw" --name testing -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="USE_YOUR_PASSWORD" -e POSTGRES_DB="agotool" -e APP_SECRET_KEY="USE_YOUR_SECRET_KEY" --volume "agotool_agotool_data:/agotool_data" --volume "agotool_dbdata:/dbdata" agotool bash
--> /opt/services/flaskapp/src/app/python/test_userinput.py

docker run --rm -it --volume "/Users/dblyon/modules/cpr/agotool/app/:/opt/services/flaskapp/src" agotool bash
docker run --rm -it --network="agotool_db_nw" --name testing -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="USE_YOUR_PASSWORD" -e POSTGRES_DB="agotool" -e APP_SECRET_KEY="USE_YOUR_SECRET_KEY" --volume "/Users/dblyon/modules/cpr/agotool/app/:/opt/services/flaskapp/src" agotool pytest -v ./app/python/test_userinput.py



### PYTEST workaround to flask crashing due to unknown reason
# run docker without preloading so the website will not work, but the connection to the DB will be established and therefore
# the python container will not crash
# set PRELOAD = False # pre-load objects DB connection necessary --> fast load
# to load DB
docker-compose up
# repeatedly call the following, while editing pytest tests (flask dies, but DB stays alive and load is quick)
docker exec -it agotool_flaskapp_1 pytest -v ./python/test_userinput.py
# Debugging
docker exec -it agotool_flaskapp_1 pytest -vx ./python/test_userinput.py --pdb
docker exec -it agotool_flaskapp_1 pytest -vx ./python/test_query.py --pdb
# Code coverage
docker exec -it agotool_flaskapp_1 pytest --cov
# failed tests run first
docker exec -it agotool_flaskapp_1 pytest -vxff ./python/test_userinput.py
### run pytest with separate container, not needing to turn off 'preload'
# atlas
docker run -it --net agotool_db_nw --env-file /home/dblyon/agotool/app/env_file -v "/home/dblyon/agotool/data/:/agotool_data" -v "/home/dblyon/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest pytest -vx ./python/test_query.py --pdb
# ody
docker run -it --net agotool_db_nw --env-file /Users/dblyon/modules/cpr/agotool/app/env_file -v "/Users/dblyon/modules/cpr/agotool/data/:/agotool_data" -v "/Users/dblyon/modules/cpr/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest pytest -vx ./python/test_query.py --pdb



# copy example data
# You can think of a trailing / on a source as meaning "copy the contents of this directory" as opposed to "copy the directory by name"
docker run --rm -it --volume /Users/dblyon/modules/cpr/agotool:/mounted_data --volume "agotool_agotool_data:/agotool_data" agotool rsync -avr /mounted_data/data/exampledata/ /agotool_data/data/exampledata

#### building working DB for STRING version_
# create DBs
docker exec -it postgres psql -U postgres -d postgres -f /agotool_data/PostgreSQL/create_DBs.psql
docker run -it --net agotool_db_nw --env-file /Users/dblyon/modules/cpr/agotool/app/env_file -v "/Users/dblyon/modules/cpr/agotool/data/:/agotool_data" -v "/Users/dblyon/modules/cpr/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest python ./python/create_SQL_tables.py
# populate DB for real
docker exec -it postgres psql -U postgres -d gostring -f /agotool_data/PostgreSQL/copy_from_file_and_index_STRING.psql
docker exec -it postgres psql -U postgres -d gostring -f /agotool_data/PostgreSQL/drop_and_rename_STRING.psql
docker exec -it postgres psql -U postgres -d gostring -f /agotool_data/PostgreSQL/temp.psql

docker run -it --net agotool_db_nw --env-file /Users/dblyon/modules/cpr/agotool/app/env_file -v "/Users/dblyon/modules/cpr/agotool/data/:/agotool_data" -v "/Users/dblyon/modules/cpr/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest pytest -vx ./python/test_query.py --pdb

docker run -it --net agotool_db_nw --env-file /home/dblyon/agotool/app/env_file -v "/home/dblyon/agotool/data/:/agotool_data" -v "/home/dblyon/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest bash
docker run -it --net agotool_db_nw --env-file /home/dblyon/agotool/app/env_file -v "/home/dblyon/agotool/data/:/agotool_data" -v "/home/dblyon/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest python
docker run -it --net agotool_db_nw --env-file /home/dblyon/agotool/app/env_file -v "/home/dblyon/agotool/data/:/agotool_data" -v "/home/dblyon/agotool/app/:/opt/services/flaskapp/src" agotool_flaskapp:latest python string_like_output.py

# change "preload" to True, change "skip_slow_downloads" to False, change "debug" to False
vim /var/www/agotool/app/python/variables.py
--> tadaaa it should work now
### scale a service like the flask-app
docker-compose up -d --scale flaskapp=2
##############################################################################
# http://agotool-api.meringlab.org/ # aquarius
# http://agotool.meringlab.org/     # atlas

# try a query from the CLI
curl -X POST "localhost:5912/api?enrichment_method=genome&taxid=9606" -d '{"foreground": "9606.ENSP00000251595%0d9606.ENSP00000322421%0d9606.ENSP00000333994"}'
curl -X POST "localhost:5912/api?enrichment_method=genome&taxid=9606" -d "9606.ENSP00000259606.ENSP00000322421"

/Users/dblyon/anaconda3/lib/gcc/x86_64-apple-darwin11.4.2/4.8.5/include-fixed/limits.h
/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1

##############################################################################
### flaskapp.conf /nginx backup for single flaskapp container/service
server {
    listen 80;
    server_name localhost;
    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

    location / {
        proxy_set_header   Host                 $host;
        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;

        proxy_pass http://flaskapp:5912;
        proxy_connect_timeout       6000;
        proxy_send_timeout          6000;
        proxy_read_timeout          6000;
        send_timeout                6000;

    }
}
##############################################################################
### flaskapp.conf / nginx for multiple containers
upstream flaskapp {
    server flaskapp_1:5912;
    server flaskapp_2:5912;
}

server {
    listen 80;
    server_name localhost;
    large_client_header_buffers 4 8m;
    client_header_buffer_size 1k;
    client_body_buffer_size     10M;
    client_max_body_size        10M;

#    location ~ \.(css|js|ico|png)$ {
#        root /var/www;
#        expires 2h;
#        access_log off;
#    }
    location ^~ /static {
        root /var/www;
        expires 2h;
        access_log off;
    }

    location / {
        proxy_set_header   Host                 $host;
        proxy_set_header   Host                 $http_host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;

        proxy_pass http://flaskapp;
        proxy_connect_timeout       6000;
        proxy_send_timeout          6000;
        proxy_read_timeout          6000;
        send_timeout                6000;
        proxy_max_temp_file_size    0;

    }
}



rsync -avP --recursive --files-from=./files_for_DB_STRINGv11.txt . /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/bak_v11
rsync -avP --recursive --files-from=./files_for_DB_STRINGv11.txt dblyon@imlslnx-atlas.uzh.ch:/home/dblyon/agotool/data/PostgreSQL/tables ./
rsync -avP --recursive --files-from=./files_for_DB_STRINGv11.txt . dblyon@san.embl.de:/home/dblyon/agotool/data/PostgreSQL/tables/

docker-compose up -d --no-deps --build service_name

docker build -t flaskapp_alpine:latest -f ./Dockerfile_alpine .

conda remove --name agotool --all
conda env create -n agotool -f conda_agotool.yml


python setup.py build_ext --inplace


conda_agotool.yml:
  - clang
  - gcc
  - libgcc

##############################################################################################################
# Protein_2_Function_and_Score_DOID_GO_BTO.txt integrated_protein2function.tsv # Protein 2 Function and Score relationships for etypes -22, -25, and -26 (GO cellular component, BTO tissues, and DOID diseases)
6239.C30G4.7    {{"GO:0043226",0.875},{"GO:0043227",0.875},{"GO:0043231",0.875},{"GO:0044424",2.96924}, ... , {"GO:0005737",2.742276},{"GO:0005777",0.703125}}      -22
10116.ENSRNOP00000049139        {{"GO:0005623",2.927737},{"GO:0044424",2.403304},{"GO:0044425",3},{"GO:0031224",3}, ... ,{"GO:0043232",0.375}}       -22
 - remove anything on blacklist (all_hidden.tsv) already happend while creating Functions_table_DOID_BTO (and all terms not present therein will be filtered out)
 - omit GO-CC (etype -22)
 Variant A.)
    using a hard cutoff of e.g. >= 3
     - create Protein_2_Function_table_DOID and
     - create Protein_2_Function_table_BTO
    and add them to Protein_2_Function_table_STRING.txt
 Variant B.)
    use continuous scores
    - translate function_name to function_enum
    - create Protein_2_FunctionEnum_and_Score_table_STRING.txt (BTO and DOID, etype -25 and -26)
    - create Taxid_2_FunctionCountArray_BTO_DOID.txt (add values to array using a function instead of merging tables)
# Protein_2_FunctionEnum_and_Score_table_STRING.txt
| 10116.ENSRNOP00000049139 | {{{0,2.927737},{3,2.403304},{4,3},{666,3}, ... ,{3000000,0.375}} |
# sum scores and scale to sum up to foreground_n
#   --> scaling_factor = sum(scores) / foreground_n
#   score * scaling_factor
# create precomputed counts per genome analogous to Taxid_2_FunctionCountArray_table_STRING.txt
# Taxid_2_FunctionCountArray_2_merge_BTO_DOID.txt
| 9606 | 19566 | {{{0,3},{3,2},{4,3},{666,3}, ... ,{3000000,1}} |
# sum scores and scale to sum up to background_n
#   --> scaling_factor = sum(scores) / background_n
#   score * scaling_factor --> and round to closest integer


# Functions_table_DOID_BTO.txt integrated_function2description.tsv # GO, BTO, and DOID function descriptions
 - add hierarchical level, year placeholder
 - merge with Functions_table
 - add things to Lineage table
-26     DOID:0050483    DOID:0050483
-26     DOID:0050662    Bestrophinopathy
-26     DOID:0060317    Lung abscess
-25     BTO:0003000     EB-1 cell
-22     GO:0099012      Neuronal dense core vesicle membrane





Protein_2_Function_table_PMID_STS download_Function_2_Description_PMID Function_table_PMID_temp Protein_2_FunctionEnum_and_Score_table_STRING Functions_table_DOID_BTO Taxid_2_FunctionCountArray_2_merge_BTO_DOID download_Interpro_descriptions



ToDo:
testing
- enrichment examples in app/python/test
- examples from website
- filter_parents
- FDR_cutoff
- genome vs compare_samples --> same result if using genome as background
-

#
Protein_2_FunctionEnum_and_Score_table_STRING



################################################################################
##### installing/restarting aGOtool
### get the code to run the python flask app from github
# clone git repo (master branch is STRING v11)
git clone https://github.com/dblyon/agotool.git
git checkout STRING_v11
cd ./agotool/app

### install anaconda (follow online instructions)
# create an enviroment using requirements in yml file
conda env create -n agotool -f conda_agotool.yml
# get rid of the conda prompt
conda config --show | grep changeps1
conda config --set changeps1 False


### push the data (flat files) from e.g. Atlas/Gaia to San/Pisces using zipped file
rsync -avP /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/bak_v11.3/STRING_v11.3_flat_files.zip dblyon@san.embl.de:/home/dblyon/agotool/data/PostgreSQL/tables/
# or alternatively rsync the txt files
cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/bak_v11.3
rsync -avP --recursive --files-from=./files_for_DB_STRINGv11.txt . dblyon@san.embl.de:/home/dblyon/agotool/data/PostgreSQL/tables/
# cd to agotool/data/PostgreSQL/tables/ and unzip files
unzip STRING_v11.3_flat_files.zip


### activate the environment (or use absolute path of python bin)
conda activate agotool
# find and select absolute path for python environment (use absolute path of proper env and add "/bin/python")
conda info -e

### compile/build the Cythonized extension module
cd agotool/app/python
# compile run_cythonized.*.so
/mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/python setup.py build_ext --inplace

### start the python flask server
cd ./agotool/app
nohup /mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/python runserver.py  &>/dev/null &
################################################################################
#### 20190618
#### building working DB for UniProt aGOtool version
# create DBs
docker exec -it postgres psql -U postgres -d agotool -f /agotool_data/PostgreSQL/create_DBs.psql
docker exec -it postgres psql -U postgres -d agotool -f /agotool_data/PostgreSQL/copy_from_file_and_index.psql
                                                        /agotool_data/PostgreSQL/copy_from_file_and_index.psql

docker exec -it postgres psql -U postgres -d agotool -f /agotool_data/PostgreSQL/drop_and_rename.psql


# remove PostgreSQL data directory, since switching from v10 to v11 results in problems
prune the system with "remove_volumes" in ""~/scripts/docker_volumes.sh "
"""
removecontainers() {
    docker stop $(docker ps -aq)
    docker rm $(docker ps -aq)
}

remove_volumes() {
    removecontainers
    docker network prune -f
    docker rmi -f $(docker images --filter dangling=true -qa)
    docker volume rm $(docker volume ls --filter dangling=true -q)
    docker rmi -f $(docker images -qa)
}
"""