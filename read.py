f = open("run/events.dat")

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

print(ee)
