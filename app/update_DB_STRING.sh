#!/usr/bin/env bash

### download resources and create SQL tables
# docker run --rm -it --name update --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py

### create DBs
docker exec -it agotool_db_1 psql -U postgres -d postgres -f /agotool_data/data/PostgreSQL/create_DBs.psql

### copy from file and index temp tables
docker exec -it agotool_db_1 psql -U postgres -d gostring -f /agotool_data/data/PostgreSQL/copy_from_file_and_index_STRING.psql

### drop old tables and rename temp tables
#docker exec -it agotool_db_1 psql -U postgres -d gostring -f /agotool_data/data/PostgreSQL/drop_and_rename_STRING.psql

### restart flask container(s), because they should preload new data from Postgres
docker restart flaskapp
