#!/bin/sh

#PBS -N network_mlewandowska

#PBS -l walltime=5:30:30

#PBS -q normal

#PBS -m abe

cd $home/neofelia/shiva/
echo 'Running ...'
python shiva.py
