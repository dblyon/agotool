#!/bin/sh
# this is aimed at fixing file permissions for Nginx on Aquarius
chmod -R 744 /home/dblyon/agotool/app/static

# on Aquarius
#~/agotool/.git/hooks$
#-rwxrwx--- 1 dblyon mering  120 May 15 13:24 post-checkout
#-rwxrwx--- 1 dblyon mering  121 May 15 13:26 post-merge
#(agotool) dblyon@aquarius:~/agotool/.git/hooks$ cat post-merge
##!/bin/sh
#chmod a+x /home/dblyon/agotool/app/static/fixpermissions.sh
#/home/dblyon/agotool/app/static/fixpermissions.sh
