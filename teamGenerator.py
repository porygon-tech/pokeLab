#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:03:19 2023
https://www.smogon.com/stats/
@author: roman
"""

import pandas as pd
import numpy as np

'''
from os import chdir, listdir
from pathlib import Path
chdir('/home/roman/LAB/MIKI')
root = Path(".")
data_path = root / 'data'
listdir(data_path)
db = pd.read_json(data_path / listdir(data_path)[0])
'''


'''
dat.keys()
dat['Moves']
dat['Checks and Counters']
dat['Abilities']
dat['Teammates']
dat['usage']
dat['Items']
dat['Raw count']
dat['Spreads']
dat['Happiness']
dat['Viability Ceiling']
'''


import requests
import re


#%%

def choosefrom(probDict,n=1):
    probs=np.array(list(probDict.values()))
    probs = probs/probs.sum()
    return np.array(list(probDict.keys()))[np.random.choice(np.arange(len(probDict)),p=probs,size=n, replace=False)]

def bestof(probDict, n=1):
    #max(spreads, key=spreads.get)
    dict_sorted = dict(sorted(probDict.items(), key=lambda item: item[1]))
    return list(dict_sorted.keys())[-n:]

#%%
html_text = requests.get('https://www.smogon.com/stats/', timeout=2).text
years = [i.replace('\"', '') for i in re.findall(r"\"\S+\-\S+/\"", html_text)]
url = 'https://www.smogon.com/stats/' + np.random.choice(years) + 'chaos/'

html_text = requests.get(url, timeout=2).text
metas = [i.replace('\"', '') for i in re.findall(r"\"\S+\.json\"", html_text)]
url = url + np.random.choice(metas)
print('fetching '+ url)
#%%
#r = requests.get('https://www.smogon.com/stats/2022-12/chaos/gen9ou-0.json')
#r = requests.get('https://www.smogon.com/stats/2022-12/chaos/gen9ou-1500.json')
#r = requests.get('https://www.smogon.com/stats/2021-03/chaos/gen8ou-1500.json')
r = requests.get(url)

j = r.json()
db = pd.DataFrame.from_dict(j)
#names = list(db.index)
mon_db = db.drop(['team type', 'cutoff', 'cutoff deviation', 'metagame', 'number of battles'])
#mon_db.loc['Gengar']

#%%
competition_level = 0.01
usage = 0
while usage < competition_level:
    randPoke = mon_db.iloc[np.random.randint(mon_db.shape[0]+1)]
    dat = randPoke.data
    usage = dat['usage']
    print(randPoke.name + '?')
    
print('I choose you, ' + randPoke.name + '!')

#%% MOVES
moves = choosefrom(dat['Moves'],4)
for i in moves: print(i)

#%% ABILITY
print(choosefrom(dat['Abilities'])[0])

#%% ITEM
print(choosefrom(dat['Items'])[0])

#%% SPREAD
print(choosefrom(dat['Spreads'])[0])

#%% TEAMMATES
randTeammates = mon_db.loc[choosefrom(dat['Teammates'],5)]
print(randTeammates)
bestof(dat['Teammates'],5)
#%%

'''
teammates_sorted = dict(sorted(dat['Teammates'].items(), key=lambda item: item[1]))
list(teammates_sorted.keys())[-2:]
teammates_sorted.values()

probs=np.array(list(dat['Teammates'].values()))
probs = probs/probs.sum()

randTeammates = mon_db.loc[np.array(list(dat['Teammates'].keys()))[np.random.choice(len(teammates_sorted),3,p=probs, replace=False)]]
randTeammates
'''
#%%


