import os
import pandas as pd
import sys

#remove the df = df.head(1) line to process everything

def run(row):
    ecms = row.ecms
    emin = row.emin*0.9
    tmin = row.tmin-1
    tmax = row.tmax+1
    id = int(row.id)
    ebeam = row.ebeam
    ecms = row.ecms

    os.system(f"mkdir /eos/user/r/rgargiul/www/babapadme/{id}")
    os.system(f"cd /eos/user/r/rgargiul/www/babapadme/{id}; /afs/cern.ch/work/r/rgargiul/padme/run_babayaga.sh {ecms} {tmin} {tmax} {emin}")
    os.system(f"python3 /afs/cern.ch/work/r/rgargiul/padme/process_babayaga.py {id}")
    os.system(f"echo -n {id},{ebeam},{ecms}, >> xs.txt")
    os.system(f"grep 'total (nb)' /eos/user/r/rgargiul/www/babapadme/{id}/run/statistics.txt | grep -o -P '(?<=:).*(?=-)' | sed 's/+//g' | sed 's/ //g' | tr -d '\n' >> xs.txt")
    os.system("echo -n , >> xs.txt")
    os.system(f"grep 'total (nb)' /eos/user/r/rgargiul/www/babapadme/{id}/run/statistics.txt | grep -o -P '(?<=-).*(?= )' |  sed 's/ //g' >> xs.txt")

os.system("echo id,ebeam,ecms,xs,xs_err > xs.txt")
df = pd.read_csv("info.csv")
#df = df.head(1)
print(df)

df.apply(lambda row: run(row), axis=1)
