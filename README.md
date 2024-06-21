code here: https://github.com/raeubaen/babayaga-fixed-target/tree/main

Cuts in babayaga are looser than analysis cuts


a run was made with nominal analysis cuts at 17 MeV, obtaining a 0.39mb cross section
time cuts, magnet shadow and many effects are missing
including a 70% efficiency to the XS, the yield/POT in data is recovered

with looser cuts the cross sections are much higher, therefore the real XS must be evaluated as bhe babayaga one * the complete efficiency after geant4, reco and selection


comments on babayaga config:
/afs/cern.ch/work/r/rgargiul/BabaYaga/babayaga << eof
fs ee
mode unweighted #per andare dentro geant4 facile
ecms $1 #depending on energy [GeV]
thmin $2 #like above [degrees]
thmax $3 #... [degrees]
zmax 40 # looser than elisa cuts on (pi-theta1-theta2), if correctly evaluated [degrees]
emin $4 #... [GeV]
nphot -1
nev 10000
path run
ntuple yes
sprb1 0.000018 #3 per mille sul fascio, traslato nel beam energy spread di un fascio equivalente al collider [GeV]
sprb2 0.000018
run
eof
