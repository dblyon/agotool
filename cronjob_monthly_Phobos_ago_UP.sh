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
### run snakemake pipeline
printf "\n ### run snakemake pipeline \n"
cd "$PYTHON_DIR" || exit
check_exit_status
"$SNAKEMAKE_EXE" -l | tr '\n' ' ' | xargs "$SNAKEMAKE_EXE" -j 10 -F
check_exit_status

### PyTest file sizes and line numbers
printf "\n### PyTest test_flatfiles.py checking updated files for size and line numbers\n"
"$PYTEST_EXE" "$TESTING_DIR"/test_flatfiles.py -p no:cacheprovider
check_exit_status

### tar and compress new files for transfer and backup
printf "\n ### tar.gz new files for transfer and backup \n"
cd "$TABLES_DIR" || exit
find . -maxdepth 1 -name '*.npy' -o -name '*_UPS_FIN*' -o -name "DF_file_dimensions_log.txt" | xargs tar -cvzf "$TAR_CURRENT"
check_exit_status
rsync -av "$TAR_CURRENT" "$TAR_BAK"
check_exit_status

### populate PostgreSQL
echo "\n### copying to PostgreSQL\n"
cd "$POSTGRES_DIR" || exit
check_exit_status
psql -d agotool -f copy_from_file_and_index.psql
check_exit_status
printf "\n ### drop and rename PostgreSQL \n"
psql -d agotool -f drop_and_rename.psql
check_exit_status

### start uWSGI and PyTest (zerg needs to be running)
printf "\n ### starting uWSGI flaskapp, sleep 4min and PyTest \n"
cd "$APP_DIR" || exit
"$UWSGI_EXE" pytest_agotool.ini &
printf "sleeping for 4min \n"
sleep 4m
printf "done sleeping \n"

### test REST API
"$PYTEST_EXE" "$TESTING_DIR"/test_API_sanity.py -p no:cacheprovider
check_exit_status

### clean up
printf "shutting down aGOtool workers"
cd "$APP_DIR" || exit
echo Q > pytest.fifo
check_exit_status

### copy files to Pisces (production server)
echo "\n ### copy files to Pisces \n"
rsync -av "$TABLES_DIR"/"$TAR_CURRENT" dblyon@pisces.meringlab.org:/home/dblyon/agotool/data/PostgreSQL/tables/"$TAR_CURRENT"
check_exit_status
### on production server, decompress files, populate DB, restart service
echo "now attempting to run script on production server cronjob_update_Pisces_ago_UP.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@pisces.meringlab.org '/home/dblyon/agotool/cronjob_monthly_Pisces_ago_UP.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown'
check_exit_status

printf "\n --- finished Cronjob --- \n"

# 1 1 1 * * /scratch/dblyon/agotool/cronjob_monthly_Phobos_ago_UP.sh >> /scratch/dblyon/agotool/data/logs/cron_monthly_snakemake_log.txt 2>&1
# 1 20 * * 0 /home/dblyon/agotool_PMID_autoupdate/agotool/cron_weekly_Phobos_ago_STRING_PMID.sh >> /home/dblyon/agotool_PMID_autoupdate/agotool/data/logs/cron_weekly_sna    kemake_log.txt 2>&1