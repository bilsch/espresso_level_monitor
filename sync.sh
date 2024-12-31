#!/usr/bin/env bash

eval "$(pyenv init -)"

set -e

venv_name="espresso_level_monitor"
mount_path="/Volumes/CIRCUITPY"

pyenv virtualenvs | grep -q $venv_name
if [ $? -ne 0 ];
then
    pyenv virtualenv $venv_name
fi

pyenv activate $venv_name
pip install -r requirements.txt

circup install --auto-file code.py 
rsync -av fonts/*.bdf* $mount_path/fonts/