#!/bin/bash

# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

TAR_CURRENT=aGOtool_flatfiles_current.tar
TAR_BAK=bak_aGOtool_flatfiles_current$(date +"%Y_%m_%d_%I_%M_%p").tar.bz2

### Header message
echo "--- Cronjob starting "$(date +"%Y_%m_%d_%I_%M_%p")" ---"

#### tar and compress previous files for backup --> commented out: since too many backups
#echo "\n### tar and compress previous files for backup\n"
#TAR_FILE_NAME=bak_aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
#cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables
##### create tar of relevant flat files
#find . -maxdepth 1 -name '*.npy' -o -name '*_UPS_FIN*' | xargs tar cvf $TAR_FILE_NAME
#check_exit_status
##### compress for quick transfer and backup, this can run in the background since it's independent of snakemake
#pbzip2 -p10 $TAR_FILE_NAME &
#check_exit_status

### run snakemake pipeline
echo "\n### run snakemake pipeline\n"
cd /scratch/dblyon/agotool/app/python
/mnt/mnemo5/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake -l | tr '\n' ' ' | xargs /mnt/mnemo5/dblyon/install/anaconda3/envs/agotoolv2/bin/snakemake -j 10 -F
check_exit_status

# add file dimensions to log for testing and debugging
cd /scratch/dblyon/agotool/app/python
/mnt/mnemo5/dblyon/install/anaconda3/envs/agotoolv2/bin/python -c 'import create_SQL_tables_snakemake; create_SQL_tables_snakemake.add_2_DF_file_dimensions_log()'

# automated testing here!!! ToDo if tests pass --> then proceed with the rest

# tar and compress new files for backup
echo "\n### tar and compress new files for backup\n"
cd /scratch/dblyon/agotool/data/PostgreSQL/tables
### create tar.gz of relevant flat files
find . -maxdepth 1 -name '*_UPS_FIN*' | xargs tar --overwrite -cvf "$TAR_CURRENT"
check_exit_status
# compress for quick transfer and backup, keep tar
pbzip2 -f -k -p10 $TAR_FILE_NAME
check_exit_status
rsync -av "$TAR_CURRENT".bz2 "$TAR_BAK"
check_exit_status

# copy files to Aquarius (production server)
echo "\n### copy files to Aquarius (production server)\n"
rsync -av /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/"$TAR_CURRENT".bz2 dblyon@aquarius.meringlab.org:/home/dblyon/agotool/data/PostgreSQL/tables/"$TAR_CURRENT".bz2
check_exit_status

# on production server, decompress files, populate DB, restart service
echo "now attempting to run script on production server cronjob_update_aGOtool_Aquarius.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
ssh dblyon@aquarius.meringlab.org '/home/dblyon/agotool/cronjob_update_aGOtool_Aquarius.sh &> /home/dblyon/agotool/data/logs/log_updates.txt & disown'
check_exit_status
### remove tar, but not bz2
rm $TAR_FILE_NAME

echo "\n--- finished Cronjob ---\n"
########################################################################################################################
### on production server "cronjob_update_aGOtool_Aquarius.sh"
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
# 1 1 1 * * /mnt/mnemo5/dblyon/agotool/cronjob_monthly_Phobos.sh >> /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt 2>&1
<<<<<<< HEAD:cronjob_monthly_Phobos.sh
########################################################################################################################
=======
########################################################################################################################
>>>>>>> cfd391b1cf56f8ac0056e1ed0401b263fee36aa8:cronjob_monthly_Atlas.sh
