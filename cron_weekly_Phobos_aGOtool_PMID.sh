#!/bin/bash

### Overview of scripts and pipelines --> for PMID autoupdate part
## ATLAS
# - run snakemake on Atlas
# - tar and compress new files for transfer and backup
# - push to Aquarius and Pisces, on San pull from Aquarius
# -




# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

TAR_CURRENT=aGOtool_PMID_pickle_current.tar.gz
TAR_BAK=bak_aGOtool_PMID_pickle_$(date +"%Y_%m_%d_%I_%M_%p").tar.gz
AFC_KS_CURRENT=AFC_KS_flat_files_current.tar
AFC_KS_BAK=bak_AFC_KS_flat_files_$(date +"%Y_%m_%d_%I_%M_%p").tar.bz2

### Header message
echo "--- Cronjob starting "$(date +"%Y_%m_%d_%I_%M_%p")" ---"

### run snakemake pipeline
echo "\n### run snakemake pipeline\n"
cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/app/python
/mnt/mnemo5/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake -l | tr '\n' ' ' | xargs /mnt/mnemo5/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake -j 10 -F
check_exit_status


# add file dimensions to log for testing and debugging
#cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/app/python
#/mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/python -c 'import create_SQL_tables_snakemake; create_SQL_tables_snakemake.add_2_DF_file_dimensions_log()'

# automated testing here!!! ToDo if tests pass --> then proceed with the rest

### tar and compress new files for transfer and backup
echo "\n### tar and compress new files for transfer and backup\n"
cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables
### create tar.gz of relevant flat files
find . -maxdepth 1 -name '*_STS_FIN.p' | xargs tar --overwrite -cvzf "$TAR_CURRENT"
check_exit_status
rsync -av "$TAR_CURRENT" "$TAR_BAK"
check_exit_status

### AFC_KS file: tar and gzip current, bz2 backup, remove tar
cd /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables
check_exit_status
tar -cf "$AFC_KS_CURRENT" ./afc_ks
check_exit_status
gzip -kf "$AFC_KS_CURRENT"
check_exit_status
pbzip2 -p10 "$AFC_KS_CURRENT"
check_exit_status
mv "$AFC_KS_CURRENT".bz2 "$AFC_KS_BAK"
check_exit_status

#### copy files to production servers
echo "\n### copy files to Aquarius (production server)\n"
### Aquarius
rsync -av /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_CURRENT" dblyon@aquarius.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_CURRENT"
check_exit_status
echo "\n### copy files to Pisces (production server)\n"
### Pisces
rsync -av /mnt/mnemo5/dblyon/agotool_PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_CURRENT" dblyon@pisces.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/"$TAR_FILE_NAME"
check_exit_status
### San --> pull instead of push

#### Production server, decompress files and restart service
### Aquarius
echo "run script on production server cron_weekly_Aquarius_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@aquarius.meringlab.org '/home/dblyon/PMID_autoupdate/agotool/cron_weekly_Aquarius_update_aGOtool_PMID.sh &>> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown'

### Pisces
echo "run script on Pisces production server cron_weekly_Pisces_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@pisces.meringlab.org '/home/dblyon/PMID_autoupdate/agotool/cron_weekly_Pisces_update_aGOtool_PMID.sh &>> /home/dblyon/PMID_autoupdate/agotool/data/logs/log_updates.txt & disown'

echo "\n--- finished Cronjob ---\n"


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