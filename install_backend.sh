#!/bin/bash

original_path=$(pwd)

#cd "$original_path"/components/common
#chmod 777 install.sh

#cd "$original_path"/components/backend
#chmod 777 install.sh
#chmod 777 start.sh

path_intall=~/GrenInHouse

mkdir -p "$path_intall"
cp -a "$original_path"/components "$path_intall"
cd "$path_intall"
mkdir -p venv_backend
cd "$path_intall"/venv_backend
python3 -m venv .venv
source "$path_intall"/venv_backend/.venv/bin/activate

pip3 install wheel flask connexion sqlalchemy==2.0.0b3 pyyaml
pip3 install connexion[swagger-ui]

cd "$path_intall"/components/common
./install.sh

cd "$path_intall"/components/backend
./install.sh
./start.sh