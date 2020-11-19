#!/bin/bash
# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181
# shellcheck disable=SC2028
### called from Phobos
### /home/dblyon/agotool/cronjob_update_aGOtool_Aquarius.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TABLES_DIR=/home/dblyon/agotool/data/PostgreSQL/tables
PYTEST_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/pytest
# UWSGI_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/uwsgi
TESTING_DIR=/home/dblyon/agotool/app/python/testing/sanity
APP_DIR=/home/dblyon/agotool/app
POSTGRES_DIR=/home/dblyon/agotool/data/PostgreSQL


### decompress files
echo "running script on production server cronjob_update_aGOtool_Aquarius.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
printf "\n### unpacking tar.gz files\n"
cd "$TABLES_DIR"
tar --overwrite -xvzf "$TABLES_DIR"/aGOtool_flatfiles_current.tar.gz
check_exit_status

### PyTest file sizes and line numbers
printf "\n### PyTest test_flatfiles.py checking updated files for size and line numbers\n"
"$PYTEST_EXE" "$TESTING_DIR"/test_flatfiles.py
check_exit_status

### copy from file to PostgreSQL
echo "\n### copying to PostgreSQL\n"
cd "$POSTGRES_DIR"
check_exit_status
psql -d agotool -p 8001 -f copy_from_file_and_index.psql
check_exit_status
### drop old tables and rename temp tables
printf "\n### drop and rename PostgreSQL\n"
cd "$POSTGRES_DIR"
psql -d agotool -p 8001 -f drop_and_rename.psql
check_exit_status
psql -d agotool -p 8001 -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agotool;"
check_exit_status

### restart uWSGI and PyTest
printf "\n### chain reloading of uWSGI flaskapp, sleep 4min and PyTest\n"
cd "$APP_DIR"
echo c > agotool_master.fifo
sleep 4m
cd "$TESTING_DIR"
"$PYTEST_EXE"
check_exit_status

#printf "\n###start uWSGI PyTest and sleep for 4min\n"
#cd "$APP_DIR"
#"$UWSGI_EXE" uwsgi_config_pytest.ini &> uwsgi_pytest_log.txt &
#sleep 4m
#printf "\n###PyTest all\n"
#cd "$TESTING_DIR"
#"$PYTEST_EXE"
#check_exit_status
#printf "\n###stopping uWSGI PyTest"
#cd "$APP_DIR"
#echo q > pytest_master.fifo
#
#### chain-reloading
#echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
#cd "$APP_DIR"
#echo c > agotool_master.fifo
#check_exit_status

#### PyTest all sanity tests
#printf "\n### Sleep 3min and PyTest all sanity tests\n"
#sleep 3m
#cd "$TESTING_DIR"
#"$PYTEST_EXE"
#check_exit_status

#### DEPRECATED
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/copy_from_file_and_index.psql