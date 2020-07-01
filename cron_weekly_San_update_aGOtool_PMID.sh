#!/bin/bash

# shellcheck disable=SC2038
# shellcheck disable=SC2164
# shellcheck disable=SC2028
# shellcheck disable=SC2181

#TAR_FILE_NAME=$1
#LOG_UPDATES=$2

echo "--- running script cron_weekly_San_update_aGOtool_PMID.sh @ "$(date +"%Y_%m_%d_%I_%M_%p")" ---"
check_exit_status () {
  if [ ! $? = 0 ]; then exit; fi
}

### pull files from Aquarius instead of pushing from Atlas
echo "\n### pull files from Aquarius\n"
rsync -av dblyon@aquarius.meringlab.org:/home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_flatfiles_current.tar /home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_flatfiles_current.tar
check_exit_status

echo "\n### unpacking tar files\n"
tar -xvf /home/dblyon/PMID_autoupdate/agotool/data/PostgreSQL/tables/aGOtool_flatfiles_current.tar
check_exit_status

echo "\n### restarting service @ $(date +'%Y_%m_%d_%I_%M_%p')\n"
cd /home/dblyon/PMID_autoupdate/agotool/app
echo c > master.fifo
check_exit_status