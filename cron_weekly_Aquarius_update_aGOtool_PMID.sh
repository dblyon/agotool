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
global_enrichment_data_current=global_enrichment_data_current.tar.gz
GED_DIR=/home/dblyon/global_enrichment_v11
# UWSGI_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/uwsgi


echo "--- running script cron_weekly_Aquarius_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
printf "\n### unpacking tar gz files\n"
cd "$TABLES_DIR" || exit
tar --overwrite -xvzf "$TABLES_DIR"/aGOtool_PMID_pickle_current.tar.gz
check_exit_status
cd "$GED_DIR" || exit
tar --overwrite -xvf "$TAR_GED_ALL_CURRENT"
check_exit_status
tar --overwrite -xzf "$global_enrichment_data_current"
check_exit_status

### restart uWSGI and PyTest
cd "$APP_DIR" || exit
echo c > PMID_master.fifo
sleep 4m
cd "$TESTING_DIR" || exit
"$PYTEST_EXE"
check_exit_status


#printf "\n###start uWSGI flask app for PyTest and sleep for 4min\n"
#cd "$APP_DIR"
#"$UWSGI_EXE" uwsgi_config_pytest.ini &> uwsgi_pytest_log.txt &
#sleep 4m
#
#printf "\n### PyTest all sanity tests\n"
#cd "$TESTING_DIR"
#"$PYTEST_EXE"
#check_exit_status
#
#printf "\n###stopping uWSGI PyTest"
#cd "$APP_DIR"
#echo q > pytest_master.fifo
#
#### chain_reloading
#echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
#cd "$APP_DIR"
#echo c > PMID_master.fifo
#check_exit_status


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