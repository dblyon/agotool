################################################################################
##### installing/restarting aGOtool
### get the code to run the python flask app from github
# clone git repo (master branch is STRING v11)
git clone https://github.com/dblyon/agotool.git
cd ./agotool/app

### install anaconda (follow online instructions)
# create an enviroment using requirements in yml file
conda env create -n agotool -f conda_agotool.yml
# get rid of the conda prompt
conda config --show | grep changeps1
conda config --set changeps1 False


### push the data (flat files) from e.g. Atlas/Gaia to San/Pisces using zipped file
rsync -avP /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/bak_v11.3/STRING_v11.3_flat_files.zip dblyon@san.embl.de:/home/dblyon/agotool/data/PostgreSQL/tables/
# or alternatively rsync the txt files
cd /mnt/mnemo5/dblyon/agotool/data/PostgreSQL/tables/bak_v11.3
rsync -avP --recursive --files-from=./files_for_DB_STRINGv11.txt . dblyon@san.embl.de:/home/dblyon/agotool/data/PostgreSQL/tables/


### activate the environment (or use absolute path of python bin)
conda activate agotool
# find and select absolute path for python environment (use absolute path of proper env and add "/bin/python")
conda info -e

### compile/build the Cythonized extension module
cd agotool/app/python
# compile run_cythonized.***.so
/mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/python setup.py build_ext --inplace

### start the python flask server
cd ./agotool/app
nohup /mnt/mnemo5/dblyon/install/anaconda3/envs/agotool/bin/python runserver.py  &>/dev/null &
################################################################################

