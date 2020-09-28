#!/bin/bash
# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181
# shellcheck disable=SC2028
### called from Phobos
### /home/dblyon/PMID_autoupdate/agotool/cron_weekly_Aquarius_update_aGOtool_PMID.sh &>> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TABLES_DIR=/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables
PYTEST_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/pytest
TESTING_DIR=/home/dblyon/PMID_autoupdate/agotool/app/python/testing/sanity
APP_DIR=/home/dblyon/PMID_autoupdate/agotool/app
TAR_GED_ALL_CURRENT=GED_all_current.tar
GED_DIR=/home/dblyon/global_enrichment_v11

echo "--- running script cron_weekly_Aquarius_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
printf "\n### unpacking tar gz files\n"
cd "$TABLES_DIR"
tar --overwrite -xvzf "$TABLES_DIR"/aGOtool_PMID_pickle_current.tar.gz
check_exit_status
cd "$GED_DIR"
tar --overwrite -xkvf "$TAR_GED_ALL_CURRENT"
check_exit_status

### PyTest file sizes and line numbers
printf "\n### PyTest test_flatfiles.py checking updated files for size and line numbers\n"
cd "$TESTING_DIR"
"$PYTEST_EXE" "$TESTING_DIR"/test_flatfiles.py
check_exit_status

### chain-reload
echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
cd "$APP_DIR"
echo c > master.fifo
check_exit_status
sleep 4m

### PyTest all sanity tests
printf "\n### PyTest all sanity tests\n"
cd "$TESTING_DIR"
"$PYTEST_EXE"
check_exit_status


# uwsgi --reload uwsgi_aGOtool_master_PID.txt
# uwsgi --touch-chain-reload uwsgi_aGOtool_master_PID.txt
#################################################################################################################################
### DEPRECATED since app is not dependent on PostgreSQL
### copy from file to PostgreSQL
#printf "\n### copying to PostgreSQL\n"
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/copy_from_file_and_index.psql
#cd /home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL
#psql -d agotool -p 8001 -f copy_from_file_and_index.psql
#check_exit_status
### drop old tables and rename temp tables
#printf "\n### drop and rename PostgreSQL\n"
#docker exec -it postgres12 psql -U postgres -d agotool -f /agotool_data/PostgreSQL/drop_and_rename.psql
#psql -d agotool -p 8001 -f drop_and_rename.psql
#check_exit_status
#psql -d agotool -p 8001 -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agotool;"
#check_exit_status
#################################################################################################################################