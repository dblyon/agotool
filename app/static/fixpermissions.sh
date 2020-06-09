#!/bin/sh
# this is aimed at fixing file permissions for Nginx on Aquarius
chmod -R 755 /home/dblyon/agotool/app/static
chmod 777 /home/dblyon/agotool/cronjob_update_aGOtool_Aquarius.sh

# on Aquarius
#~/agotool/.git/hooks$
#-rwxrwx--- 1 dblyon mering  120 May 15 13:24 post-checkout
#-rwxrwx--- 1 dblyon mering  121 May 15 13:26 post-merge
#(agotool) dblyon@aquarius:~/agotool/.git/hooks$ cat post-merge
##!/bin/sh
#chmod a+x /home/dblyon/agotool/app/static/fixpermissions.sh
#/home/dblyon/agotool/app/static/fixpermissions.sh

# ### don't forget to
# chmod 777 post-merge
# chmod 777 post-checkout