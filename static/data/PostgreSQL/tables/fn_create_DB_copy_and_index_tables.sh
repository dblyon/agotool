#!/bin/bash
psql -h localhost -d postgres -c "DROP DATABASE agotool;"
psql -h localhost -d postgres -c "CREATE DATABASE agotool;"

psql -h localhost -d agotool -c "CREATE TABLE functions (
    type text,
    name text,
    an text);"
psql -h localhost -d agotool -c "CREATE TABLE function_2_definition (
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
    function text);"    
psql -h localhost -d agotool -c "CREATE TABLE protein_secondary_2_primary_an (
    sec text,
    pri text);"
psql -h localhost -d agotool -c "CREATE TABLE protein_2_og (
    an text,
    og text);"

psql -h localhost -d agotool -c "COPY functions FROM '/Users/dblyon/Downloads/tables/Functions_table.txt';"
psql -h localhost -d agotool -c "COPY function_2_definition FROM '/Users/dblyon/Downloads/tables/Function_2_definition_table.txt';"
psql -h localhost -d agotool -c "COPY go_2_slim FROM '/Users/dblyon/Downloads/tables/GO_2_Slim_table.txt';"
psql -h localhost -d agotool -c "COPY ogs FROM '/Users/dblyon/Downloads/tables/OGs_table.txt';"
psql -h localhost -d agotool -c "COPY og_2_function FROM '/Users/dblyon/Downloads/tables/OG_2_Function_table.txt';"
psql -h localhost -d agotool -c "COPY ontologies FROM '/Users/dblyon/Downloads/tables/Ontologies_table.txt';"
psql -h localhost -d agotool -c "COPY protein_2_function FROM '/Users/dblyon/Downloads/tables/Protein_2_Function_table.txt';"
psql -h localhost -d agotool -c "COPY protein_secondary_2_primary_an FROM '/Users/dblyon/Downloads/tables/Protein_Secondary_2_Primary_AN_table.txt';"
psql -h localhost -d agotool -c "COPY protein_2_og FROM '/Users/dblyon/Downloads/tables/Protein_2_OG_table.txt';"

psql -h localhost -d agotool -c "CREATE INDEX functions_an_idx ON functions(an);"
psql -h localhost -d agotool -c "CREATE INDEX function_2_definition_an_idx ON function_2_definition(an);"
psql -h localhost -d agotool -c "CREATE INDEX go_2_slim_an_idx ON go_2_slim(an);"
psql -h localhost -d agotool -c "CREATE INDEX ogs_og_idx ON ogs(og);"
psql -h localhost -d agotool -c "CREATE INDEX og_2_function_og_idx ON og_2_function(og);"
psql -h localhost -d agotool -c "CREATE INDEX ontologies_child_idx ON ontologies(child);"
psql -h localhost -d agotool -c "CREATE INDEX ontologies_direct_idx ON ontologies(direct);"
psql -h localhost -d agotool -c "CREATE INDEX ontologies_type_idx ON ontologies(type);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_function_an_idx ON protein_2_function(an);"
psql -h localhost -d agotool -c "CREATE INDEX protein_secondary_2_primary_an_sec_idx ON protein_secondary_2_primary_an(sec);"
psql -h localhost -d agotool -c "CREATE INDEX protein_2_og_an_idx ON protein_2_og(an);"