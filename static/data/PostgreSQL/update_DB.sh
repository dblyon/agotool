#!/bin/bash
sudo systemctl start postgresql

### create DB
sudo -u postgres psql postgres -c "CREATE DATABASE agotool OWNER dblyon;"

### populate DB
### download resources, create SQL tables, copy from file and index DB
python3 /var/www/agotool/static/python/update_manager.py # recently added, sanity check

### create user 'agotool' with read-only-access to the DB
sudo -u postgres psql agotool -c "CREATE USER agotool;"
sudo -u postgres psql agotool -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO agotool;"

### start PostgreSQL
sudo systemctl start postgresql

### /home/dblyon/bin/update_agotool.sh is the master script, contents below
##!/bin/bash
#/var/www/agotool/static/data/PostgreSQL/update_DB.sh >> /var/www/agotool/logs/update.log
#pkill -f -u agotool runserver.py
#cd /var/www/agotool
#python runserver.py >> /var/www/agotool/logs/runserver.log 2>&1 &