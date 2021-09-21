import numpy as np
import matplotlib.pyplot as plt
from numpy import floor

def samplecolors(n, type='hex',palette=plt.cm.plasma):
	if type == 'hex':
		return list(map(plt.cm.colors.rgb2hex, list(map(palette, np.linspace(1,0,n)))))
	elif type == 'rgba':
		return list(map(palette, np.linspace(1,0,n)))

def dmg(pwr, attack, defense, mod=1, lv=100):
	a = floor(2 * lv / 5 + 2)
	base = (floor(floor(a*pwr*attack/defense)/50)+2)
	rolls = floor(np.array((base*0.85,base)))
	return(floor(mod*rolls))

def fulldmg(pwr, attack, defense, mod=1, lv=100):
	a = floor(2 * lv / 5 + 2)
	base = (floor(floor(a*pwr*attack/defense)/50)+2)
	rands = np.array(range(85,101))/100
	rolls = floor(base*rands)
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



def plotseries(l, l_names=None):
	fig = plt.figure(); ax = fig.add_subplot(111)
	ax.plot(range(len(l)), l)
	if l_names:
		ax.set_xticklabels(l_names)
	plt.show()


'''
def analyze(
	basehp=20,
	basedef=230,
	defnature='+',
	total_evs=252,
	basepower=90,
	atkstat = stat(130,ev=252, nature='+'),
	modifier=1.5):
	dpercents=np.zeros((253,2))
	hp_dmg   =np.zeros((253,2))
	ev_range = np.array(range(253))
	for def_evs in ev_range:
		hpstat = stat_hp(basehp,ev=total_evs-def_evs)
		defstat = stat(basedef,ev=def_evs, nature=defnature)
		d = dmg(basepower,atkstat,defstat,modifier)
		dpercents[def_evs,:] = d/hpstat*100
		hp_dmg[def_evs,:] = d
		#print(def_evs,total_evs-def_evs, d[1]/hpstat)
	#optDef = np.argmin(dpercents,axis=0)
	#optDef = np.argmin(dpercents[:,1])
	optDef = np.argmin(dpercents.mean(axis=1))
	optHP  = 252 - optDef
	fig = plt.figure(); ax = fig.add_subplot(111)
	ax.plot(ev_range, dpercents[:,0], label = 'Lo')
	ax.plot(ev_range, dpercents[:,1], label = 'Hi')
	ax.set_title(str(basehp) + ' base HP, ' + str(basedef) + ' base Def. Optimal: ' + str(optDef) + 'Def; ' + str(optHP) + 'HP.')
	ax.set_xlabel('defense EVs', labelpad=10)
	ax.set_ylabel('% damage', labelpad=10)
	ax.legend(loc='lower left')
	plt.show()
'''




def analyze_full(
	basehp=20,
	basedef=230,
	defnature='+',
	total_evs=252,
	basepower=90,
	atkstat = stat(130,ev=252, nature='+'),
	modifier=1.5):
	palette = samplecolors(16)
	dpercents=np.zeros((253,16))
	hp_dmg   =np.zeros((253,16))
	ev_range = np.array(range(253))
	for def_evs in ev_range:
		hpstat = stat_hp(basehp,ev=total_evs-def_evs)
		defstat = stat(basedef,ev=def_evs, nature=defnature)
		d = fulldmg(basepower,atkstat,defstat,modifier)
		dpercents[def_evs,:] = d/hpstat*100
		hp_dmg[def_evs,:] = d
		#print(def_evs,total_evs-def_evs, d[1]/hpstat)
	optDef = np.argmin(dpercents.mean(axis=1))
	optHP  = 252 - optDef
	fig = plt.figure(); ax = fig.add_subplot(111)
	for x in range(16):
		ax.plot(ev_range, dpercents[:,x], label = str(x), color=palette[x])
	ax.set_title(str(basehp) + ' base HP, ' + str(basedef) + ' base Def. Optimal: ' + str(optDef) + 'Def; ' + str(optHP) + 'HP.')
	ax.set_xlabel('defense EVs', labelpad=10)
	ax.set_ylabel('% damage', labelpad=10)
	ax.legend(loc='lower left')
	plt.show()
	return(dpercents)


def showdata(mat, color=plt.cm.plasma, norm = False, symmetry=False):
	mat = np.copy(mat)
	if symmetry:
		top = np.max([np.abs(np.nanmax(mat)),np.abs(np.nanmin(mat))])
		plt.imshow(mat.astype('float32'), interpolation='none', cmap='seismic',vmax=top,vmin=-top)
	elif norm:
		plt.imshow(mat.astype('float32'), interpolation='none', cmap=color,vmax=1,vmin=0)
	else:
		plt.imshow(mat.astype('float32'), interpolation='none', cmap=color)
	plt.colorbar()
	plt.show()



def damagematrix(
	basehp=20,
	basedef=230,
	defnature='+',
	total_evs=504,
	basepower=90,
	atkstat = stat(130,ev=252, nature='+'),
	modifier=1.5):
	M = np.zeros((253,253))
	for j in range(253):
		for i in range(253):
			if (i+j)>total_evs:
				M[i,j]=np.NaN
			else:
				hpstat = stat_hp(basehp,ev=i)
				defstat = stat(basedef,ev=j, nature=defnature)
				d = np.array(fulldmg(basepower,atkstat,defstat,modifier)).mean()
				M[i,j] = d/hpstat
	evspread = np.unravel_index(np.nanargmin(M), M.shape)
	return(M,evspread)


	


#======================= krookodile earthquake vs shuckle =========================
dperc=analyze_full(
	basehp=20,
	basedef=230,
	defnature=1,
	total_evs=252,
	basepower=100,
	atkstat = stat(117,ev=252, nature=1),
	modifier=1.5)


avgs = dperc.mean(axis=1)
plotseries(avgs)


atkstat = stat(117, ev=252)
hpstat = stat_hp(20,ev=248)
defstat = stat(230, ev=8)
dmg(100,atkstat,defstat,1.5)/hpstat*100
fulldmg(100,atkstat,defstat,1.5)

#==================================================================================
#================================ DAMAGE MATRIX ===================================
#======================= nihilego power gem vs Porygon2 =========================
M, evspread = damagematrix(
	basehp=85,
	basedef=90,
	defnature=1,
	total_evs=252,
	basepower=100,
	atkstat = stat(127,ev=252),
	modifier=1.5)

print('optimal: ' + str(evspread[0]) + 'HP, ' + str(evspread[1]) + 'Def')


M = damagematrix(
	basehp=85,
	basedef=90,
	defnature=1,
	total_evs=328,
	basepower=100,
	atkstat = stat(127,ev=252),
	modifier=1.5)


#======================= nihilego power gem vs Porygon2 =========================
analyze_full(
	basehp=85,
	basedef=90,
	defnature=1,
	total_evs=252,
	basepower=100,
	atkstat = stat(127,ev=252),
	modifier=1.5)

atkstat = stat(117, ev=252)
hpstat = stat_hp(20,ev=248)
defstat = stat(230, ev=8)
dmg(100,atkstat,defstat,1.5)/hpstat*100
#=======================================================================

#nihilego vs wobbuffet
M, evspread = damagematrix(
	basehp=190,
	basedef=58,
	defnature='+',
	total_evs=252,
	basepower=90,
	atkstat = stat(110,ev=252),
	modifier=1.5)
evspread

showdata(M)







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
fulldmg(100,atkstat,defstat,1.5)
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
defnature='+'
total_evs=252
basepower=90
atkstat = stat(130,ev=252, nature='+')
modifier=1.5

dpercents=np.zeros((253,16))
hp_dmg   =np.zeros((253,16))
ev_range = np.array(range(253))
for def_evs in ev_range:
	hpstat = stat_hp(basehp,ev=total_evs-def_evs)
	defstat = stat(basedef,ev=def_evs, nature=defnature)
	#d = dmg(basepower,atkstat,defstat,modifier)
	d = fulldmg(basepower,atkstat,defstat,modifier)
	dpercents[def_evs,:] = d/hpstat*100
	hp_dmg[def_evs,:] = d
	#print(def_evs,total_evs-def_evs, d[1]/hpstat)


fig = plt.figure(); ax = fig.add_subplot(111)
ax.plot(ev_range, dpercents[:,0], label = 'Lo')
ax.plot(ev_range, dpercents[:,1], label = 'Hi')
ax.set_title(str(basehp) + ' base HP, ' + str(basedef) + ' base Def')
ax.set_xlabel('EVs for defence', labelpad=10)
ax.set_ylabel('% damage', labelpad=10)
ax.legend(loc='lower left')

print(np.argmin(dpercents,axis=0))


plt.show()
#================================================












analyze(basehp=80,basedef=100,defnature='+',total_evs=252,basepower=90,atkstat = stat(130,ev=252, nature='+'),modifier=1.5)
















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
