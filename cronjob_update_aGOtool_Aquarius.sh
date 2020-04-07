#!/bin/bash

# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

TAR_FILE_NAME=$1
#LOG_UPDATES=$2

check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

# shellcheck disable=SC2028
echo "\n### unpacking tar bzip files\n"
pbzip2 -p8 -dc "$TAR_FILE_NAME" | tar x
check_exit_status

## check if file sizes etc. are as expected --> done on Atlas side, adding data to DF_file_dimensions.txt
#echo "\n### checking updated files for size\n"
#python /home/dblyon/agotool/app/python/obsolete_check_file_dimensions.py
#check_exit_status

# copy from file to PostgreSQL
echo "\n### copying to PostgreSQL\n"
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/copy_from_file_and_index.psql
cd /home/dblyon/agotool/data/PostgreSQL
psql -d agotool -p 8001 -f copy_from_file_and_index.psql
check_exit_status

# drop old tables and rename temp tables
echo "\n### drop and rename PostgreSQL\n"
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/drop_and_rename.psql
psql -d agotool -p 8001 -f drop_and_rename.psql
check_exit_status

# restart service (hard restart)
echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
# cd /mnt/mnemo5/dblyon/agotool/app
# /mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/uwsgi --reload uwsgi_aGOtool_master_PID.txt
#docker exec -it
