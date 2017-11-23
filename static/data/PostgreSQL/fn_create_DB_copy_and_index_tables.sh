#!/bin/bash
psql -h localhost -d postgres -c "DROP DATABASE agotool;"
psql -h localhost -d postgres -c "CREATE DATABASE agotool;"

psql -h localhost -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text,
    definition text);"
psql -h localhost -d agotool -c "CREATE TABLE go_2_slim (
    an text,    
    slim boolean);"
psql -h localhost -d agotool -c "CREATE TABLE ogs (
    og text,    
    description text);"
psql -h localhost -d agotool -c "CREATE TABLE og_2_function (
    og text,
    function text);"
psql -h localhost -d agotool -c "CREATE TABLE ontologies (
    child text,
    parent text,
    direct boolean,
    type integer);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_function (
    an text,
    function text ARRAY);"    
psql -h localhost -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -h localhost -d agotool -c "COPY functions FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/tables/Functions_table.txt';"
psql -h localhost -d agotool -c "COPY go_2_slim FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/tables/GO_2_Slim_table.txt';"
psql -h localhost -d agotool -c "COPY ogs FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/static/OGs_table_static.txt';"
psql -h localhost -d agotool -c "COPY og_2_function FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/static/OG_2_Function_table_static.txt';"
psql -h localhost -d agotool -c "COPY ontologies FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/tables/Ontologies_table.txt';"
psql -h localhost -d agotool -c "COPY protein_2_function FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/tables/Protein_2_Function_table.txt';"
psql -h localhost -d agotool -c "COPY protein_secondary_2_primary_an FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/tables/Protein_Secondary_2_Primary_AN_table.txt';"
psql -h localhost -d agotool -c "COPY protein_2_og FROM '/Users/dblyon/modules/cpr/agotool/static/data/PostgreSQL/static/Protein_2_OG_table_static.txt';"

psql -h localhost -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -h localhost -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"