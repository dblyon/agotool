#!/usr/bin/env bash

### download resources and create SQL tables
docker run --rm -it --name update --volume "agotool_agotool_data:/agotool_data" agotool_flaskapp python ./app/python/update_manager.py

### copy from file and index temp tables
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/copy_from_file_and_index.psql

### drop old tables and rename temp tables
docker exec -it agotool_db_1 psql -U postgres -d agotool -f /agotool_data/data/PostgreSQL/drop_and_rename.psql
