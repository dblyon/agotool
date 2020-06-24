#!/bin/bash

# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

### Header message
echo "--- Cronjob starting "$(date +"%Y_%m_%d_%I_%M_%p")" ---"

### run snakemake pipeline
echo "\n### run snakemake pipeline\n"
cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/app/python
/mnt/mnemo5/dblyon/install/anaconda3/envs/snake/bin/snakemake -l | tr '\n' ' ' | xargs /mnt/mnemo5/dblyon/install/anaconda3/envs/snake/bin/snakemake -j 10 -F
check_exit_status

# add file dimensions to log for testing and debugging
#cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/app/python
#/mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/python -c 'import create_SQL_tables_snakemake; create_SQL_tables_snakemake.add_2_DF_file_dimensions_log()'

# automated testing here!!! ToDo if tests pass --> then proceed with the rest

### tar and compress new files for transfer and backup
echo "\n### tar and compress new files for transfer and backup\n"
TAR_FILE_NAME=bak_aGOtool_PMID_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables
### create tar of relevant flat files

find . -maxdepth 1 -name '*_STS_FIN.p' | xargs tar cvf $TAR_FILE_NAME
check_exit_status
### compress for quick transfer
pbzip2 -p10 $TAR_FILE_NAME
check_exit_status
# copy files to Aquarius (production server)
echo "\n### copy files to Aquarius (production server)\n"
rsync -av /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_FILE_NAME".bz2 dblyon@aquarius.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_flatfiles_current.tar.bz2
check_exit_status
### delete tar but keep tar.bz2
rm $TAR_FILE_NAME


### AFC_KS file: tar and gzip current, bz2 backup, remove tar
cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables
check_exit_status
tar -cf AFC_KS_flat_files_current.tar ./afc_ks
check_exit_status
gzip -kf AFC_KS_flat_files_current.tar
check_exit_status
pbzip2 -p10 AFC_KS_flat_files_current.tar
check_exit_status
mv AFC_KS_flat_files_current.tar.bz2 bak_AFC_KS_flat_files_$(date +"%Y_%m_%d_%I_%M_%p").tar.bz2
check_exit_status


## tar and compress new files for backup
#echo "\n### tar and compress new files for backup\n"
#TAR_FILE_NAME=bak_aGOtool_PMID_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
#cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables
## create tar of relevant flat files
#find . -maxdepth 1 -name '*_STS_FIN.p' | xargs tar cvf $TAR_FILE_NAME
#check_exit_status
#
## compress for quick transfer and backup, keep tar
#pbzip2 -k -p10 $TAR_FILE_NAME
#check_exit_status


# on production server, decompress files, populate DB, restart service
echo "now attempting to run script on production server cron_weekly_Aquarius_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@aquarius.meringlab.org '/home/dblyon/PMID_autoupdate/agotool/cron_weekly_Aquarius_update_aGOtool_PMID.sh &> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown'
echo "\n--- finished Cronjob ---\n"


########################################################################################################################
### on production server "cron_weekly_Aquarius_update_aGOtool_PMID.sh"
# pbzip2 -p10 -dc $TAR_FILE_NAME | tar x
# check if files are similar size of larger than previously
# copy from file SQL
# alter tables SQL

# restart service (hard restart)
# cd /home/dblyon/agotool/app (# cd /mnt/mnemo5/dblyon/agotool/app)
# /home/dblyon/anaconda3/envs/agotool/bin/uwsgi --reload uwsgi_aGOtool_master_PID.txt (# /mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/uwsgi --reload uwsgi_aGOtool_master_PID.txt)
# --> dockerize
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
# 1 1 1 * * /mnt/mnemo5/dblyon/agotool/cron_weekly_Atlas_aGOtool_PMID.sh >> /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt 2>&1
########################################################################################################################