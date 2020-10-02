#!/bin/bash
# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181
### crontab
### 1 13 * * 1 /home/dblyon/PMID_autoupdate/agotool/cron_weekly_San_update_aGOtool_PMID.sh >> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_cron_weekly_San_update_aGOtool_PMID.txt 2>&1
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TABLES_DIR=/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables
APP_DIR=/home/dblyon/PMID_autoupdate/agotool/app
PYTEST_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/pytest
UWSGI_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/uwsgi
TESTING_DIR=/home/dblyon/PMID_autoupdate/agotool/app/python/testing/sanity
TAR_GED_ALL_CURRENT=GED_all_current.tar
global_enrichment_data_current=global_enrichment_data_current.tar.gz
GED_DIR=/san/DB/dblyon/global_enrichment_v11

echo "--- running script cron_weekly_San_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
### pull files from Aquarius instead of pushing from Atlas
printf "\n### pull files from Aquarius\n"
rsync -av dblyon@aquarius.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_PMID_pickle_current.tar.gz "$TABLES_DIR"/aGOtool_PMID_pickle_current.tar.gz
check_exit_status
rsync -av dblyon@aquarius.meringlab.org:/home/dblyon/global_enrichment_v11/"$TAR_GED_ALL_CURRENT" "$GED_DIR"/"$TAR_GED_ALL_CURRENT"
check_exit_status

### decompress files
echo "\n### unpacking tar.gz files\n"
cd "$TABLES_DIR"
tar --overwrite -xvzf "$TABLES_DIR"/aGOtool_PMID_pickle_current.tar.gz
check_exit_status
cd "$GED_DIR"
check_exit_status
tar --overwrite -xvf "$TAR_GED_ALL_CURRENT"
check_exit_status
tar --overwrite -xzf "$global_enrichment_data_current"
check_exit_status

printf "\n###start uWSGI flask app for PyTest and sleep for 4min\n"
cd "$APP_DIR"
"$UWSGI_EXE" uwsgi_config_pytest.ini &> uwsgi_pytest_log.txt &
sleep 4m

printf "\n### PyTest all sanity tests\n"
cd "$TESTING_DIR"
"$PYTEST_EXE"
check_exit_status

printf "\n###stopping uWSGI PyTest"
cd "$APP_DIR"
echo q > pytest_master.fifo

### chain_reloading
echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
cd "$APP_DIR"
echo c > PMID_master.fifo
check_exit_status

#### PyTest file sizes and line numbers
#printf "\n### PyTest test_flatfiles.py checking updated files for size and line numbers\n"
#cd "$TESTING_DIR"
#check_exit_status
#"$PYTEST_EXE" "$TESTING_DIR"/test_flatfiles.py
#check_exit_status
#
#### chain_reloading
#echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
#cd "$APP_DIR"
#check_exit_status
#echo c > master.fifo
#check_exit_status
#sleep 4m
#
#### PyTest all sanity tests
#printf "\n### PyTest all sanity tests\n"
#cd "$TESTING_DIR"
#check_exit_status
#"$PYTEST_EXE"
#check_exit_status