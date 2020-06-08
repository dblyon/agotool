#!/bin/sh
##### Aquarius for agotool_PMID_autoupdate
#### vim /home/dblyon/PMID_autoupdate/agotool/app/static/fixpermissions.sh
### this is aimed at fixing file permissions for Nginx on Aquarius
chmod -R 755 /home/dblyon/PMID_autoupdate/agotool/app/static
chmod 777 /home/dblyon/PMID_autoupdate/agotool/cron_weekly_Aquarius_update_aGOtool_PMID.sh

# ### cd /home/dblyon/PMID_autoupdate/agotool/.git/hooks
# ### vim post-checkout and post-merge
# #!/bin/sh
# chmod a+x /home/dblyon/PMID_autoupdate/agotool/app/static/fixpermissions.sh
# /home/dblyon/PMID_autoupdate/agotool/app/static/fixpermissions.sh