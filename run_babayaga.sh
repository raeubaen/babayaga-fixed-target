#!/bin/bash

#example: source run_babayaga.sh 0.017 78 102 0.006

/afs/cern.ch/work/r/rgargiul/BabaYaga/babayaga << eof
fs ee
mode unweighted
ecms $1
thmin $2
thmax $3
zmax 18
emin $4
nphot -1
nev 10000
path run
ntuple yes
sprb1 0.000018
sprb2 0.000018
run
eof
