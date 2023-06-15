import pandas as pd
import numpy as np
import re

from os import chdir
from pathlib import Path
chdir('/home/roman/LAB/MIKI') #this line is for Spyder IDE only
root = Path(".")
import teamGen

#gen9metas = [re.findall(r"gen9\S+", i) for i in teamGen.get_metas()][0]
#meta = np.random.choice(gen9metas)
meta = np.random.choice(teamGen.get_metas())
db = teamGen.get_meta_json(meta)
top = teamGen.filterbest(db)


#METHOD 1: select random pokemon and 5 allies based on coupling data
randPoke = top.loc[np.random.choice(top.index)]
print(teamGen.instanceOfPoke(randPoke))

friends = teamGen.recommendTeammates(randPoke)
for friend in friends:
	print(teamGen.instanceOfPoke(db.loc[friend]))


#METHOD 2:
f2 = teamGen.makeF2(top)
f3 = teamGen.makeF3(f2)
f4 = teamGen.makeF4(f3)
n = len(top)

#A:
m=f3.copy()
ix = np.unravel_index(np.random.choice(np.prod(m.shape),p=m.flatten()), m.shape)
ix = list(ix)
while len(ix) < 6:
  p = f4[tuple(np.random.choice(ix,3))].copy()
  p /= p.sum()
  if np.isnan(p).sum() == 0:
    i = np.random.choice(n,p=p)
    if not np.isin(i, ix):
      ix.append(i)

for i in ix:
  poke = db.loc[str(top.index[i])]
  print(teamGen.instanceOfPoke(poke))



#B
m=f2.copy() # can be f2,f3 or f4
ix = np.unravel_index(np.random.choice(np.prod(m.shape),p=m.flatten()), m.shape)
ix = list(ix)
while len(ix) < 6:
  p = f3[tuple(np.random.choice(ix,2))].copy()
  p /= p.sum()
  if np.isnan(p).sum() == 0:
    i = np.random.choice(n,p=p)
    if not np.isin(i, ix):
      ix.append(i)

for i in ix:
  poke = db.loc[str(top.index[i])]
  print(teamGen.instanceOfPoke(poke))


#EASY METHOD (3)

db = teamGen.get_meta_json('gen8ou-0.json', year='2022-02/')
top = teamGen.filterbest(db,competition_level = 0.005)

f = open("temp_team.txt", "w")
f.write(teamGen.makeTeam(top))
f.close()

f = open("temp_team.txt", "r")
team_1 = f.read()
f.close()













best_darkpulse_users = teamGen.filterbymove(top,'darkpulse')
leadname = np.random.choice(best_darkpulse_users.index)
m=f3[np.where(top.index == leadname)[0][0]].copy() # can be f2,f3 or f4
m /= m.sum()
ix = np.unravel_index(np.random.choice(np.prod(m.shape),p=m.flatten()), m.shape)
ix = list(ix)
top.iloc[ix]


print(teamGen.instanceOfPoke(top.loc[leadname]))
for i in ix:
  #poke = db.loc[str(top.index[i])]
  poke = db.loc[top.index[i]]
  print(teamGen.instanceOfPoke(poke))