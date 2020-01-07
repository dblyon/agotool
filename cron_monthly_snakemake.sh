#!/bin/sh

# tar and compress previous files for backup
echo "\n### tar and compress previous files for backup"
TAR_FILE_NAME=bak_aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables
# create tar of relevant flat files
find . -maxdepth 1 -name "*.npy" -o -name "*_UPS_FIN.txt" | xargs tar cvf $TAR_FILE_NAME
# compress for quick transfer and backup
pbzip2 -p24 $TAR_FILE_NAME &


# run snakemake pipeline
echo "\n### run snakemake pipeline"
cd /mnt/mnemo5/dblyon/agotool/app/python
/mnt/mnemo5/dblyon/install/anaconda3/envs/snake/bin/snakemake -l | tr '\n' ' ' | xargs /mnt/mnemo5/dblyon/install/anaconda3/envs/snake/bin/snakemake -j 24 -F

# tar and compress new files for backup
echo "\n### tar and compress new files for backup"
TAR_FILE_NAME=aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables
# create tar of relevant flat files
find . -maxdepth 1 -name "*.npy" -o -name "*_UPS_FIN.txt" | xargs tar cvf $TAR_FILE_NAME
# compress for quick transfer and backup
pbzip2 -k -p20 $TAR_FILE_NAME


# copy files to Aquarius (production server)
echo "\n### copy files to Aquarius (production server)"
rsync -av /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/$TAR_FILE_NAME dblyon@aquarius.meringlab.org:/home/dblyon/agotool/data/PostgreSQL/tables/
echo "\n--- finished cron job ---\n"

############### on production server
### on the python side do this, but how to trigger upon new files?
# pbzip2 -dc $TAR_FILE_NAME | tar x
# check if files are similar size of larger than previously
# copy from file SQL
# alter tables SQL

# restart service (hard restart)
#cd /mnt/mnemo5/dblyon/agotool/app
#/mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/uwsgi --reload uwsgi_aGOtool_master_PID.txt
# --> dockerize


### cron commands
# crontab -e --> modify
# crontab -l --> list
# crontab -r --> remove

### contents of crontab for dblyon
#MAILTO="dblyon@gmail.com" --> only if output not redirected, use log file instead
### dblyon inserted cronjob for automated aGOtool updates
## testing 10:05 am
# 40 11 4 * * /mnt/mnemo5/dblyon/agotool/cron_monthly_snakemake.sh > /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt
# 1 1 1 * * /mnt/mnemo5/dblyon/agotool/cron_monthly_snakemake.sh > /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt
