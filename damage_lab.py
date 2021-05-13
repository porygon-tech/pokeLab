import numpy as np
import matplotlib.pyplot as plt
from numpy import floor

def dmg(pwr, attack, defense, mod=1, lv=100):
	a = floor(2 * lv / 5 + 2)
	base = (floor(floor(a*pwr*attack/defense)/50)+2)
	rolls = floor(np.array((base*0.85,base)))
	return(floor(mod*rolls))

dmg(100,atkstat,defstat,1.5)

def stat(base,ev=0,iv=31,lv=100, nature=1):
	if nature=='+':
		nature=1.1
	elif nature=='-':
		nature=0.9
	return(floor((floor((2*base+iv+floor(ev/4))*lv/100)+5)*nature))


def stat_hp(base,ev=0,iv=31,lv=100):
	return(floor((2*base+iv+floor(ev/4))*lv/100)+lv+10)


#------------------------------------
atkstat = stat(100)
defstat = stat(100)
hpstat = stat_hp(100)
dmg(100,atkstat,defstat)[1]/hpstat
#------------------------------------


#--------- adamant krookodile earthquake vs slaking -------
atkstat = stat(117, ev=252, nature='+')
hpstat = stat_hp(150,ev=16)
defstat = stat(100, ev=236, nature='+')
dmg(100,atkstat,defstat,1.5)/hpstat*100
#----------------------------------------------------------



#--------- modest espeon psychic vs bold blissey -------
atkstat = stat(130, ev=252, nature='+')
hpstat = stat_hp(255,ev=252)
defstat = stat(135, ev=4, nature=1)
dmg(90,atkstat,defstat,1.5)/hpstat*100
#----------------------------------------------------------


#================================================
basehp=20
basedef=230
total_evs=252
basepower=90
atkstat = stat(130,ev=252, nature='+')
modifier=1.5

dpercents=np.zeros((253,2))
dmgpoints  =np.zeros((253,2))
ev_range = np.array(range(253))
for def_evs in ev_range:
	hpstat = stat_hp(basehp,ev=total_evs-def_evs)
	defstat = stat(basedef,ev=def_evs, nature='+')
	d = dmg(basepower,atkstat,defstat,modifier)
	dpercents[def_evs,:] = d/hpstat*100
	dmgpoints[def_evs,:] = d
	#print(def_evs,total_evs-def_evs, d[1]/hpstat)


fig = plt.figure(); ax = fig.add_subplot(111)
ax.plot(ev_range, dmgpoints[:,0], label = 'Lo')
ax.plot(ev_range, dmgpoints[:,1], label = 'Hi')
ax.set_title(str(basehp) + ' base HP, ' + str(basedef) + ' base Def')
ax.set_xlabel('EVs for defence', labelpad=10)
ax.set_ylabel('% damage', labelpad=10)
ax.legend(loc='lower left')

print(np.argmin(dmgpoints,axis=0))


plt.show()
#================================================





#================================================
from scipy.optimize import minimize, minimize_scalar
basehp=50
basedef=130

'''
def damageopt((def_evs,hp_evs),basehp,basedef):
	#dmg(100,stat(100,ev=252, nature='+'),stat(basedef,ev=def_evs, nature='+'))[1]/stat_hp(basehp,ev=252-def_evs)
	dmg(100,stat(100,ev=252, nature='+'),stat(basedef,ev=def_evs, nature='+'))[1]/stat_hp(basehp,ev=hp_evs)
'''

def damageopt(def_evs,basehp,basedef):
	return(dmg(100,stat(100,ev=252, nature='+'),stat(basedef,ev=def_evs, nature='+'))[1]/stat_hp(basehp,ev=252-def_evs)*100)
	
damageopt(128,100,100)

minimize(damageopt)

res=minimize(damageopt,128, (100,100), bounds=[[0,225]])


#-------------------
def f(x, k, c):
	return((x-k)**(2*c))

minimize(f, 3, (1,2))
#-------------------
