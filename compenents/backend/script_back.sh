#!/bin/bash

#incluir comprobacion para crear el venv solo si no existe en el directorio

path_intall=~/GrrenInHouse
cd $path_intall
mkdir -p venv_backend
cd venv_backend
python3 -m venv .venv
source .venv/bin/activate
pip install sqlalchemy==2.0.0b3