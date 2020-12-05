#!/bin/bash
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
TAR_CURRENT=aGOtool_flatfiles_current.tar.gz
TAR_BAK=bak_aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar.gz
PYTEST_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/pytest
SNAKEMAKE_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/snakemake
UWSGI_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/uwsgi
TESTING_DIR=/scratch/dblyon/agotool/app/python/testing/sanity
APP_DIR=/scratch/dblyon/agotool/app
TABLES_DIR=/scratch/dblyon/agotool/data/PostgreSQL/tables
PYTHON_DIR=/scratch/dblyon/agotool/app/python
POSTGRES_DIR=/scratch/dblyon/agotool/data/PostgreSQL
echo "--- Cronjob starting "$(date +"%Y_%m_%d_%I_%M_%p")" ---"

### restart uWSGI and PyTest
printf "\n### chain reloading of uWSGI flaskapp, sleep 4min and PyTest\n"
cd "$APP_DIR" || exit
"$UWSGI_EXE" uwsgi_config_master.ini &
sleep 4m
cd "$TESTING_DIR" || exit
"$PYTEST_EXE"
check_exit_status
echo q > agotool_master.fifo
check_exit_status

### copy files to Aquarius (production server)
echo "\n### copy files to Aquarius (production server)\n"
rsync -av "$TABLES_DIR"/"$TAR_CURRENT" dblyon@aquarius.meringlab.org:/home/dblyon/agotool/data/PostgreSQL/tables/"$TAR_CURRENT"
check_exit_status
### on production server, decompress files, populate DB, restart service
echo "now attempting to run script on production server cronjob_update_aGOtool_Aquarius.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@aquarius.meringlab.org '/home/dblyon/agotool/cronjob_update_aGOtool_Aquarius.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown'
check_exit_status
echo "\n--- finished Cronjob ---\n"
