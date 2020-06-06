#!/bin/bash

# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

#TAR_FILE_NAME=$1
#LOG_UPDATES=$2

check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

# shellcheck disable=SC2028
echo "\n### unpacking tar bzip files\n"
pbzip2 -p8 -dc /home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_flatfiles_current.tar.bz2 | tar x
check_exit_status

## check if file sizes etc. are as expected --> done on Atlas side, adding data to DF_file_dimensions.txt
#echo "\n### checking updated files for size\n"
#python /home/dblyon/PMID_autoupdate/agotool/app/python/obsolete_check_file_dimensions.py
#check_exit_status

# copy from file to PostgreSQL
#echo "\n### copying to PostgreSQL\n"
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/copy_from_file_and_index.psql
#cd /home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL
#psql -d agotool -p 8001 -f copy_from_file_and_index.psql
#check_exit_status

# drop old tables and rename temp tables
#echo "\n### drop and rename PostgreSQL\n"
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/drop_and_rename.psql
#psql -d agotool -p 8001 -f drop_and_rename.psql
#check_exit_status
#psql -d agotool -p 8001 -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agotool;"
#check_exit_status

# restart service (hard restart)
#docker exec -it
echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
cd /home/dblyon/PMID_autoupdate/agotool/app
/home/dblyon/anaconda3/envs/agotool/bin/uwsgi --reload uwsgi_aGOtool_master_PID.txt
check_exit_status
