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
        --> github/bitbucket notifies Dockerhug
        --> Dockerhub builds image
        --> missing piece: server pulls image and starts it up

# Lars automatic updates/webhooks
bitbucket/github
    webhooks on C++ repo
Dockerhub
    build settings
        trigger URL
paste webhook m dockerhub to bitbucket
##############################################################################