import uproot
import pandas as pd
import sys
import numpy as np
import os
import pylorentz
import sys

id = int(sys.argv[1])

df = pd.read_csv("info.csv")
enbeam = df[df["id"] == id].ebeam.iloc[0]
ecms = df[df["id"] == id].ecms.iloc[0]

gamma = enbeam/ecms
beta = np.sqrt(1 - pow(gamma, -2))

workfolder  = f"/eos/user/r/rgargiul/www/babapadme/"

f = open(f"{workfolder}/{id}/run/events.dat")
c = 0
d = 0
n = 0

ee, xe, ye, ze, ep, xp, yp, zp = [], [], [], [], [], [], [], []

for l in f.readlines():
    if "EVENT" in l:
      n = 1
      c = 0
      d = 0
      continue
    if d == 1:
      if c == 2:
        d = 0
        n = 0
        continue
      if c == 0:
        ke = l.split()        
        ee.append(float(ke[0]))
        xe.append(float(ke[1]))
        ye.append(float(ke[2]))
        ze.append(float(ke[3]))
      if c == 1:
        kp = l.split()
        ep.append(float(kp[0]) )
        xp.append(float(kp[1]))
        yp.append(float(kp[2]))
        zp.append(float(kp[3]))
      c += 1
      continue
    if n == 1:
      d = 1
      continue

ele = pylorentz.Momentum4(ee, xe, ye, ze).boost(0, 0, -1, beta=beta).components.T
pos = pylorentz.Momentum4(ep, xp, yp, zp).boost(0, 0, -1, beta=beta).components.T

#calchep example
#Events       P1_3 [Gev]        P2_3 [Gev]        P3_1 [Gev]        P3_2 [Gev]        P3_3 [Gev]        P4_1 [Gev]        P4_2 [Gev]        P4_3 [Gev]     Q_factor   alpha_QCD  Color chains
#1.000E+00  2.6281000000E-01  0.0000000000E+00 -6.3203490019E-03  5.0796903795E-03  1.4947607890E-01  6.3203490019E-03 -5.0796903795E-03  1.1333392110E-01| 1.000E+00  5.211E-01 

header = f"#CalcHEP-like output from BabaYaga \n""#Type 2 -> 2+photons\n#Initial_state\nP1_3={enbeam}  P2_3=-0.000000E+00\nStrFun1=\"IDK\"\nStrFun2=\"IDK\"\n"\
"#PROCESS   -11(E) 11(e) -> 11(e) -11(E) + photons\n"\
"#MASSES  5.1100000000E-04 5.1100000000E-04 5.1100000000E-04 5.1100000000E-04\n"\
"#Cross_section(Width) n.a. \n"\
f"#Number_of_events   {len(ele)}\n"\
"#Sum_of_weights   n.a. n.a.\n"\
"#Events       P1_3 [Gev]        P2_3 [Gev]        P3_1 [Gev]        P3_2 [Gev]        P3_3 [Gev]        P4_1 [Gev]        P4_2 [Gev]        P4_3 [Gev]     Q_factor   alpha_QCD  Color chains"

open(f"{workfolder}/{id}/header.dat", "w").write(header)

ones = np.ones((len(ele)))

calchep_like = pd.DataFrame({"ev": ones, "p13": ones*enbeam, "p23": ones*0, "p31": ele[:, 1], "p32": ele[:, 2], "p33": ele[:, 3], "p41": pos[:, 1], "p42": pos[:, 2], "p43": pos[:, 3]})
calchep_like.columns = ["ev", "p13", "p23", "p31", "p32", "p33", "p41", "p42", "p43", "]

calchep_like.to_csv(f"{workfolder}/{id}/calchep_like.csv", index=None, header=False, sep=" ")

os.system(f"cat {workfolder}/{id}/header.dat {workfolder}/{id}/calchep_like.csv > {workfolder}/output_{id}.txt")

f = uproot.recreate(f"{workfolder}/bhabha_gen_{id}.root")
f["events"] = {
"e_mom": np.sqrt(ele[:, 0]**2 - (0.511e-3)**2), 
"e_comp": ele[:, 1:], 
"p_mom": np.sqrt(pos[:, 0]**2 - (0.511e-3)**2), 
"p_comp": pos[:, 1:], 
}
f.close()
