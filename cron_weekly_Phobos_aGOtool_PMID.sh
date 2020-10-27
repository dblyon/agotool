#!/bin/bash
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}
### Overview of scripts and pipelines --> for PMID autoupdate part
### Phobos
# - run snakemake on Phobos /home/dblyon/agotool_PMID_autoupdate/agotool
# - tar and gz compress new files for transfer and backup
# - push to Aquarius and Pisces, on San pull from Aquarius
TAR_CURRENT=aGOtool_PMID_pickle_current.tar.gz
TAR_BAK=bak_aGOtool_PMID_pickle_$(date +"%Y_%m_%d_%I_%M_%p").tar.gz
global_enrichment_data_current=global_enrichment_data_current.tar.gz
# global_enrichment_data_bak=bak_global_enrichment_data_$(date +"%Y_%m_%d_%I_%M_%p").tar.gz
populate_classification_schema_current=populate_classification_schema_current.sql.gz
# populate_classification_schema_bak=populate_classification_schema_$(date +"%Y_%m_%d_%I_%M_%p").sql.gz
TAR_GED_ALL_CURRENT=GED_all_current.tar
TAR_GED_ALL_BAK=BAK_GED_all_$(date +"%Y_%m_%d_%I_%M_%p").tar
GED_DIR=/home/dblyon/global_enrichment_v11
APP_DIR=/home/dblyon/agotool_PMID_autoupdate/agotool/app
PYTHON_DIR=/home/dblyon/agotool_PMID_autoupdate/agotool/app/python
TABLES_DIR=/home/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables
# SNAKEMAKE_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake
SNAKEMAKE_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/snakemake
# PYTEST_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/pytest
PYTEST_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/pytest
# UWSGI_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/agotoolv2/bin/uwsgi
UWSGI_EXE=/mnt/mnemo4/dblyon/install/anaconda3/envs/cron/bin/uwsgi
TESTING_DIR=/home/dblyon/agotool_PMID_autoupdate/agotool/app/python/testing/sanity

echo "--- Cronjob starting "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
printf "\n### run snakemake pipeline\n"
cd "$PYTHON_DIR"
"$SNAKEMAKE_EXE" -l | tr '\n' ' ' | xargs "$SNAKEMAKE_EXE" -j 10 -F
check_exit_status

### start uWSGI and PyTest
cd "$APP_DIR"
# echo c > PMID_master.fifo
"$UWSGI_EXE" uwsgi_config_PMID_autoupdates.ini &
sleep 4m
cd "$TESTING_DIR"
"$PYTEST_EXE"
check_exit_status
echo q > PMID_master.fifo
check_exit_status

#### tar and compress new files for transfer and backup
printf "\n### tar and compress new files for transfer and backup\n"
cd "$TABLES_DIR"
check_exit_status
#### create tar.gz of relevant flat files
find . -maxdepth 1 -name "*_STS_FIN.p" -o -name "DF_file_dimensions_log.txt" -o -name "DF_global_enrichment_file_stats_log.txt"| xargs tar --overwrite -cvzf "$TAR_CURRENT"
check_exit_status
rsync -av "$TAR_CURRENT" "$TAR_BAK"
check_exit_status
### AFC_KS file: tar and gzip current
cd "$TABLES_DIR"
check_exit_status
tar -cvf "$TAR_GED_ALL_CURRENT" "$global_enrichment_data_current" "$populate_classification_schema_current" "DF_global_enrichment_file_stats_log.txt"
check_exit_status
rsync -av "$TAR_GED_ALL_CURRENT" "$TAR_GED_ALL_BAK"
check_exit_status

#### copy files to production servers
printf "\n### copy files to Aquarius (production server)\n"
### San --> does pull instead of push via cronjob, data on Aquarius
### Aquarius
rsync -av "$TABLES_DIR"/"$TAR_CURRENT" dblyon@aquarius.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_CURRENT"
check_exit_status
rsync -av "$TABLES_DIR"/"$TAR_GED_ALL_CURRENT" dblyon@aquarius.meringlab.org:"$GED_DIR"/"$TAR_GED_ALL_CURRENT"
check_exit_status

printf "\n### copy files to Pisces (production server)\n"
### Pisces
rsync -av "$TABLES_DIR"/"$TAR_CURRENT" dblyon@pisces.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_FILE_NAME"
check_exit_status
rsync -av "$TABLES_DIR"/"$TAR_GED_ALL_CURRENT" dblyon@pisces.meringlab.org:"$GED_DIR"/"$TAR_GED_ALL_CURRENT"
check_exit_status

#### Production server, decompress files and restart service
### Aquarius
echo "run script on production server cron_weekly_Aquarius_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@aquarius.meringlab.org '/home/dblyon/PMID_autoupdate/agotool/cron_weekly_Aquarius_update_aGOtool_PMID.sh &>> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown'
check_exit_status
### Pisces
echo "run script on Pisces production server cron_weekly_Pisces_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@pisces.meringlab.org '/home/dblyon/PMID_autoupdate/agotool/cron_weekly_Pisces_update_aGOtool_PMID.sh &>> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown'
check_exit_status
printf "\n--- finished Cronjob ---\n"
############################################################
##### Cronjob OVERVIEW

### Crontab Atlas
## at 01:01 (1 AM) 1st day of every month
# 1 1 1 * * /mnt/mnemo5/dblyon/agotool/cronjob_monthly_Atlas.sh >> /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt 2>&1
## at 20:01 (8 PM) every Sunday
# 1 20 * * 0 /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/cron_weekly_Phobos_aGOtool_PMID.sh >> /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/log_cron_weekly_snakemake.txt 2>&1

### Crontab San
## at 01:01 (1 PM) every Monday
# 1 13 * * 1 /home/dblyon/PMID_autoupdate/agotool/cron_weekly_San_update_aGOtool_PMID.sh >> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_cron_weekly_San_update_aGOtool_PMID.txt 2>&1

### GitLab.com
## at 07:01 (7 AM) every Monday
# 1 7 * * 1 Weekly Monday morning schedule for aGOtool PMID autoupdate --> PMID_autoupdate branch

### Cheat Sheet
#* * * * * command to be executed
#- - - - -
#| | | | |
#| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
#| | | ------- Month (1 - 12)
#| | --------- Day of month (1 - 31)
#| ----------- Hour (0 - 23)
#------------- Minute (0 - 59)
############################################################
### DEPRECATED since --> built into Snakemake
### add file dimensions to log for testing and debugging
#cd "$PYTHON_DIR"
#"$PYTHON_EXE"  -c 'import create_SQL_tables_snakemake; create_SQL_tables_snakemake.add_2_DF_file_dimensions_log()'
#check_exit_status
