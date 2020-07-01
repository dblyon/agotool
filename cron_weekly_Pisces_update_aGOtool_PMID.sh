#!/bin/bash
# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

#TAR_FILE_NAME=$1
#LOG_UPDATES=$2

echo "--- running script cron_weekly_Aquarius_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

# shellcheck disable=SC2028
echo "\n### unpacking tar.gz files\n"
tar -xvzf /home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_PMID_pickle_current.tar.gz
check_exit_status

## check if file sizes etc. are as expected --> done on Atlas side, adding data to DF_file_dimensions.txt
#echo "\n### checking updated files for size\n"
#python /home/dblyon/PMID_autoupdate/agotool/app/python/obsolete_check_file_dimensions.py
#check_exit_status

echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
cd /home/dblyon/PMID_autoupdate/agotool/app
echo c > master.fifo
check_exit_status
