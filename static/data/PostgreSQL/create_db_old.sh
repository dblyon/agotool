#!/usr/bin/bash
sudo systemctl start postgresql

### create DB --> create_db.sql
### CREATE DATABASE metaprot OWNER postgres;
#sudo -u postgres psql postgres -f create_db.sql
sudo -u postgres psql postgres -c "CREATE DATABASE metaprot OWNER postgres;"

### populate DB
### su -u postgres psql -U postgres metaprot < metaprot_agotool.pgsql
### or rebuild it from scratch since probably faster
python /agotool/static/python/models.py

### create user 'guest' with read-only access to the DB --> create_user.sql
### CREATE USER guest;
### GRANT SELECT ON ALL TABLES IN SCHEMA public TO guest;
# sudo -u postgres psql postgres -f create_user.sql
sudo -u postgres psql postgres -c "CREATE USER guest;"
sudo -u postgres psql postgres -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO guest;"

sudo systemctl start postgresql



# cp /Users/dblyon/modules/cpr/metaprot/sql/deprecated_models.py /Users/dblyon/Downloads/agotool_docker/agotool/static/python
# cp /Users/dblyon/modules/cpr/metaprot/sql/deprecated_db_config.py /Users/dblyon/Downloads/agotool_docker/agotool/static/python

#/usr/local/bin/psql -p5432 -U postgres -c "CREATE DATABASE metaprot OWNER = postgres";
# psql -U postgres -c "CREATE DATABASE metaprot";
# sudo -u postgres psql postgres
