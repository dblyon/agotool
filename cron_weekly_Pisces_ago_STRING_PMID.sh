#!/bin/bash
### called from Phobos
### /home/dblyon/PMID_autoupdate/agotool/cron_weekly_Pisces_ago_STRING_PMID.sh &>> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TABLES_DIR=/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables
TABLES_DIR_Digamma=/home/dblyon/agotool/data/PostgreSQL/tables
APP_DIR=/home/dblyon/PMID_autoupdate/agotool/app
PYTEST_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/pytest
TESTING_DIR=/home/dblyon/PMID_autoupdate/agotool/app/python/testing/sanity
TAR_GED_ALL_CURRENT=GED_all_current.tar
global_enrichment_data_current=global_enrichment_data_current.tar.gz
GED_DIR=/home/dblyon/global_enrichment_v11
UWSGI_EXE=/home/dblyon/anaconda3/envs/agotoolv2/bin/uwsgi

echo "--- running script cron_weekly_Pisces_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"

### decompress files
echo "\n### unpacking tar.gz files\n"
cd "$TABLES_DIR" || exit
tar --overwrite -xvzf "$TABLES_DIR"/aGOtool_PMID_pickle_current.tar.gz
check_exit_status
cd "$GED_DIR" || exit
tar --overwrite -xvf "$TAR_GED_ALL_CURRENT"
check_exit_status
tar --overwrite -xzf "$global_enrichment_data_current"
check_exit_status

### test flat files
printf "\n PyTest flat files \n"
cd "$TESTING_DIR" || exit
"$PYTEST_EXE" test_flatfiles.py
check_exit_status

### restart uWSGI
printf "\n restart uWSGI and PyTest \n"
cd "$APP_DIR" || exit
"$UWSGI_EXE" vassal_agotool_STRING.ini
sleep 4m

## test API
printf "\n PyTest REST API \n"
cd "$TESTING_DIR" || exit
"$PYTEST_EXE" test_API_sanity.py
check_exit_status

### push files to Digamma
printf "\n rsync push files from Pisces to Digamma"
rsync -av "$TABLES_DIR"/aGOtool_PMID_pickle_current.tar.gz dblyon@digamma.embl.de:"$TABLES_DIR_Digamma"/aGOtool_PMID_pickle_current.tar.gz
rsync -av "$GED_DIR"/"$TAR_GED_ALL_CURRENT" dblyon@digamma.embl.de:"$GED_DIR"/"$TAR_GED_ALL_CURRENT"

echo "now attempting to run update script on Digamma cron_weekly_Digamma_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@digamma.embl.de '/home/dblyon/agotool/cron_weekly_Digamma_ago_STRING_PMID.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown'
check_exit_status

printf " --- done --- "
