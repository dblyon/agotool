#!/usr/bin/env bash
parallel -a /home/dblyon/agotool/app/python/pvalues.all_pmids.tsv --gnu -j36 --bar --pipepart --block 1M --recstart "
" --joblog split_log.txt "python /home/dblyon/agotool/app/python/add_infos_afc.py > /home/dblyon/agotool/data/PostgreSQL/tables/temp/part_{#}.txt"