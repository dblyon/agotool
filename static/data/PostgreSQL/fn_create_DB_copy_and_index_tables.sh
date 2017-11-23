#!/bin/bash
psql -d postgres -c "DROP DATABASE agotool;"
psql -d postgres -c "CREATE DATABASE agotool;"

psql -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text,
    definition text);"
psql -d agotool -c "CREATE TABLE go_2_slim (
    an text,    
    slim boolean);"
psql -d agotool -c "CREATE TABLE ogs (
    og text,    
    description text);"
psql -d agotool -c "CREATE TABLE og_2_function (
    og text,
    function text);"
psql -d agotool -c "CREATE TABLE ontologies (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -d agotool -c "CREATE TABLE protein_2_function (
    an text,
    function text ARRAY);"    
psql -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -d agotool -c "\copy functions FROM '/var/www/agotool/static/data/PostgreSQL/tables/Functions_table.txt';"
psql -d agotool -c "\copy go_2_slim FROM '/var/www/agotool/static/data/PostgreSQL/tables/GO_2_Slim_table.txt';"
psql -d agotool -c "\copy ogs FROM '/var/www/agotool/static/data/PostgreSQL/static/OGs_table_static.txt';"
psql -d agotool -c "\copy og_2_function FROM '/var/www/agotool/static/data/PostgreSQL/static/OG_2_Function_table_static.txt';"
psql -d agotool -c "\copy ontologies FROM '/var/www/agotool/static/data/PostgreSQL/tables/Ontologies_table.txt';"
psql -d agotool -c "\copy protein_2_function FROM '/var/www/agotool/static/data/PostgreSQL/tables/Protein_2_Function_table.txt';"
psql -d agotool -c "\copy protein_secondary_2_primary_an FROM '/var/www/agotool/static/data/PostgreSQL/tables/Protein_Secondary_2_Primary_AN_table.txt';"
psql -d agotool -c "\copy protein_2_og FROM '/var/www/agotool/static/data/PostgreSQL/static/Protein_2_OG_table_static.txt';"

psql -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"