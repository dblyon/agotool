#!/bin/sh

# tar and compress previous files for backup
TAR_FILE_NAME=bak_aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables
# create tar of relevant flat files
find . -maxdepth 1 -name "*.npy" -o -name "*_UPS_FIN.txt" | xargs tar cvf TAR_FILE_NAME
# compress for quick transfer and backup
pbzip2 -p24 $TAR_FILE_NAME &

# run snakemake pipeline
cd /mnt/mnemo5/dblyon/agotool/app/python
/mnt/mnemo5/dblyon/install/anaconda3/envs/snake/bin/snakemake -l | tr '\n' ' ' | xargs /mnt/mnemo5/dblyon/install/anaconda3/envs/snake/bin/snakemake -j 24 -F

# tar and compress new files for backup
TAR_FILE_NAME=bak_aGOtool_flatfiles_$(date +"%Y_%m_%d_%I_%M_%p").tar
cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables
# create tar of relevant flat files
find . -maxdepth 1 -name "*.npy" -o -name "*_UPS_FIN.txt" | xargs tar cvf TAR_FILE_NAME
# compress for quick transfer and backup
pbzip2 -p20 $TAR_FILE_NAME

# check if files are similar size of larger than previously


### cron commands
# crontab -e
# crontab -l

### contents of crontab for dblyon
#MAILTO="dblyon@gmail.com"
### dblyon inserted cronjob for automated aGOtool updates
# minute (0-59), hour (0-23), day of the month (1-31), month (1-12), day of the week (0-6, Sunday is 0)
# on the first day of the month at 1:01 a.m. run Snakemake pipeline
# 1 1 1 * * dblyon ~/agotool/cron_monthly_snakemake.sh

## testing 10:05 am
# 40 11 4 * * /mnt/mnemo5/dblyon/agotool/cron_monthly_snakemake.sh > /mnt/mnemo5/dblyon/agotool/log_cron_monthly_snakemake.txt
