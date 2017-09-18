#!/bin/bash
psql -h localhost -d postgres -c "DROP DATABASE agotool;"
psql -h localhost -d postgres -c "CREATE DATABASE agotool;"
psql -h localhost -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text
    );"
psql -h localhost -d agotool -c "COPY protein_secondary_2_primary_an FROM '/Volumes/Speedy/PostgreSQL/tables/Protein_Secondary_2_Primary_AN_table.txt';"
psql -h localhost -d agotool -c "CREATE INDEX protein_secondary_2_primary_an_sec_idx ON protein_secondary_2_primary_an(sec);"
