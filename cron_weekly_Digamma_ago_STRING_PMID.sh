#!/bin/bash

### crontab
### 1 13 * * 1 /home/dblyon/agotool/cron_weekly_Digamma_ago_STRING_PMID.sh >> /home/dblyon/agotool/data/logs/log_cron_weekly_Digamma_update_aGOtool_PMID.txt 2>&1
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TABLES_DIR_Aquarius=/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables
TABLES_DIR_Digamma=/home/dblyon/agotool/data/PostgreSQL/tables
APP_DIR=/home/dblyon/agotool/app
PYTEST_EXE=/home/dblyon/anaconda3/envs/agotool/bin/pytest
TESTING_DIR=/home/dblyon/agotool/app/python/testing/sanity
TAR_GED_ALL_CURRENT=GED_all_current.tar
global_enrichment_data_current=global_enrichment_data_current.tar.gz
GED_DIR=/home/dblyon/global_enrichment_v11
UWSGI_EXE=/home/dblyon/anaconda3/envs/agotool/bin/uwsgi

echo "--- running script cron_weekly_Digamma_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"

### decompress files
echo "\n### unpacking tar.gz files\n"
cd "$TABLES_DIR_Digamma" || exit
tar --overwrite -xvzf "$TABLES_DIR_Digamma"/aGOtool_PMID_pickle_current.tar.gz
check_exit_status
cd "$GED_DIR" || exit
check_exit_status
tar --overwrite -xvf "$TAR_GED_ALL_CURRENT"
check_exit_status
tar --overwrite -xzf "$global_enrichment_data_current"
check_exit_status

### test flat files
printf "\n PyTest flat files \n"
cd "$TESTING_DIR" || exit
"$PYTEST_EXE" test_flatfiles.py
check_exit_status

### start a uWSGI testing app (additional sanity check, since switching back to chain-reloading)
printf "\n restart uWSGI and PyTest \n"
cd "$APP_DIR" || exit
"$UWSGI_EXE" pytest_agotool_STRING.ini &
sleep 4m
### test API
printf "\n PyTest REST API \n"
cd "$TESTING_DIR" || exit
"$PYTEST_EXE" test_API_sanity.py --url testing
check_exit_status
## shutdown uWSGI flask app
cd "$APP_DIR" || exit
echo q > pytest.fifo
check_exit_status

### restart uWSGI
printf "\n restart uWSGI and PyTest \n"
cd "$APP_DIR" || exit
#"$UWSGI_EXE" vassal_agotool_STRING.ini
echo c > ago_STRING_vassal.fifo
sleep 4m

## test API
printf "\n PyTest REST API \n"
cd "$TESTING_DIR" || exit
"$PYTEST_EXE" test_API_sanity.py
check_exit_status

printf " --- done --- "
