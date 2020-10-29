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
# PYTEST_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/pytest
# SNAKEMAKE_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake
# PYTHON_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/python
# UWSGI_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/uwsgi
PYTEST_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/pytest
SNAKEMAKE_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/snakemake
PYTHON_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/python
UWSGI_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/uwsgi
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
# echo c > agotool_master.fifo
"$UWSGI_EXE" uwsgi_config_master.ini &
sleep 4m
cd "$TESTING_DIR"
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
