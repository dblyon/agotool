#!/bin/bash

### called from Phobos
### /home/dblyon/agotool/cronjob_monthly_Aquarius_ago_UP.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TABLES_DIR=/home/dblyon/agotool/data/PostgreSQL/tables
PYTEST_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/pytest
UWSGI_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/uwsgi
TESTING_DIR=/home/dblyon/agotool/app/python/testing/sanity
APP_DIR=/home/dblyon/agotool/app
POSTGRES_DIR=/home/dblyon/agotool/data/PostgreSQL


### decompress files
echo "running script on production server cronjob_update_aGOtool_Aquarius.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
printf "\n### unpacking tar.gz files\n"
cd "$TABLES_DIR" || exit
tar --overwrite -xvzf "$TABLES_DIR"/aGOtool_flatfiles_current.tar.gz
check_exit_status

### PyTest file sizes and line numbers
printf "\n### PyTest test_flatfiles.py checking updated files for size and line numbers\n"
"$PYTEST_EXE" "$TESTING_DIR"/test_flatfiles.py -p no:cacheprovider
check_exit_status

### copy from file to PostgreSQL
echo "\n### copying to PostgreSQL\n"
cd "$POSTGRES_DIR" || exit
check_exit_status
psql -d agotool -p 8001 -f copy_from_file_and_index.psql
check_exit_status
### drop old tables and rename temp tables
printf "\n### drop and rename PostgreSQL\n"
cd "$POSTGRES_DIR" || exit
psql -d agotool -p 8001 -f drop_and_rename.psql
check_exit_status
psql -d agotool -p 8001 -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agotool;"
check_exit_status

### restart uWSGI and PyTest
printf "\n### chain reloading of uWSGI flaskapp, sleep 4min and PyTest\n"
cd "$APP_DIR" || exit
# echo c > agotool_master.fifo
"$UWSGI_EXE" vassal_agotool.ini
sleep 4m

### test REST API
cd "$TESTING_DIR" || exit
"$PYTEST_EXE" "$TESTING_DIR"/test_API_sanity.py -p no:cacheprovider
check_exit_status