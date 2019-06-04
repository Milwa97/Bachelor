#!/bin/sh

#PBS -N network_mlewandowska

#PBS -l cput=10:00:30

#PBS -q normal

#PBS -m abe

cd ${HOME}/shiva/
echo 'Running ...'
python shiva.py
