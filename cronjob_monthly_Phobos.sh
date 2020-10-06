#!/bin/bash
# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

TAR_CURRENT=aGOtool_flatfiles_current.tar.gz
TAR_BAK=bak_aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar.gz

PYTEST_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/pytest
SNAKEMAKE_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake
PYTHON_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/python
UWSGI_EXT=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/uwsgi
TESTING_DIR=/scratch/dblyon/agotool/app/python/testing/sanity
TABLES_DIR=/scratch/dblyon/agotool/data/PostgreSQL/tables
PYTHON_DIR=/scratch/dblyon/agotool/app/python
POSTGRES_DIR=/scratch/dblyon/agotool/data/PostgreSQL

echo "--- Cronjob starting "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
### run snakemake pipeline
printf "\n### run snakemake pipeline\n"
cd "$PYTHON_DIR"
check_exit_status
"$SNAKEMAKE_EXE" -l | tr '\n' ' ' | xargs "$SNAKEMAKE_EXE" -j 10 -F
check_exit_status

### PyTest file sizes and line numbers
printf "\n### PyTest test_flatfiles.py checking updated files for size and line numbers\n"
"$PYTEST_EXE" "$TESTING_DIR"/test_flatfiles.py
check_exit_status

### tar and compress new files for transfer and backup
printf "\n### tar.gz new files for transfer and backup\n"
cd "$TABLES_DIR"
find . -maxdepth 1 -name '*.npy' -o -name '*_UPS_FIN*' -o -name "DF_file_dimensions_log.txt" | xargs tar -cvzf "$TAR_CURRENT"
check_exit_status
rsync -av "$TAR_CURRENT" "$TAR_BAK"
check_exit_status

### populate local PostgreSQL
echo "\n### copying to PostgreSQL\n"
cd "$POSTGRES_DIR"
check_exit_status
psql -d agotool -f copy_from_file_and_index.psql
check_exit_status
printf "\n### drop and rename PostgreSQL\n"
psql -d agotool -f drop_and_rename.psql
check_exit_status

### restart uWSGI and PyTest
printf "\n### chain reloading of uWSGI flaskapp, sleep 4min and PyTest\n"
cd "$APP_DIR"
echo c > agotool_master.fifo
sleep 4m
cd "$TESTING_DIR"
"$PYTEST_EXE"
check_exit_status

#### PyTest start uWSGI-flask, test, and quit
#printf "\n###start uWSGI PyTest and sleep for 4min\n"
#cd "$APP_DIR"
#"$UWSGI_EXE" uwsgi_config_pytest.ini &> uwsgi_pytest_log.txt &
#sleep 4m
#printf "\n###PyTest all\n"
#cd "$TESTING_DIR"
#check_exit_status
#"$PYTEST_EXE"
#check_exit_status
#printf "\n###stopping uWSGI PyTest"
#cd "$APP_DIR"
#echo q > pytest_master.fifo

#### start uWSGI flask app
#printf "\n###start uWSGI flask app and sleep for 3min\n"
#cd "$APP_DIR"
#"$UWSGI_EXT" uwsgi_config_master.ini
#sleep3
#
#### PyTest
#printf "\n###PyTest everything\n"
#cd "$TESTING_DIR"
#"$PYTEST_EXE"
#check_exit_status
#
#### stop uWSGI PyTest
#printf "\n###stop uWSGI PyTest\n"
#cd "$APP_DIR"
#echo q > master.fifo # also works: "$UWSGI_EXT" --stop uwsgi_aGOtool_master_PID.txt

### copy files to Aquarius (production server)
echo "\n### copy files to Aquarius (production server)\n"
rsync -av "$TABLES_DIR"/"$TAR_CURRENT" dblyon@aquarius.meringlab.org:/home/dblyon/agotool/data/PostgreSQL/tables/"$TAR_CURRENT"
check_exit_status

### on production server, decompress files, populate DB, restart service
echo "now attempting to run script on production server cronjob_update_aGOtool_Aquarius.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@aquarius.meringlab.org '/home/dblyon/agotool/cronjob_update_aGOtool_Aquarius.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown'
check_exit_status

echo "\n--- finished Cronjob ---\n"
########################################################################################################################
########################################################################################################################
### cron commands
# crontab -e --> modify
# crontab -l --> list
# crontab -r --> remove

### contents of crontab for dblyon
#MAILTO="dblyon@gmail.com" --> only if output not redirected, use log file instead
### dblyon inserted cronjob for automated aGOtool updates
## testing 10:05 am
# 1 1 1 * * /mnt/mnemo5/dblyon/agotool/cronjob_monthly_Phobos.sh >> /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt 2>&1
########################################################################################################################
########################################################################################################################