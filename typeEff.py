import numpy as np
#		NOR	FGH	FLY	POI	GRN	ROC	BUG	GHO	STL	FIR	WAT	GRA	ELC	PSY	ICE	DRA	DAK	FAY
typenames = ('NORMAL','FIGHTING','FLYING','POISON','GROUND','ROCK','BUG','GHOST','STEEL','FIRE','WATER','GRASS','ELECTRIC','PSYCHIC','ICE','DRAGON','DARK','FAIRY')
n = len(typenames)

NORMAL = [1,1,1,1,1,0.5,1,0,0.5,1,1,1,1,1,1,1,1,1]
FIGHTING = [2,1,1,0.5,0.5,2,0.5,0,2,1,1,1,1,0.5,2,1,2,0.5]
FLYING = [1,2,1,1,1,0.5,2,1,0.5,1,1,2,0.5,1,1,1,1,1]
POISON = [1,1,1,0.5,0.5,0.5,1,0.5,0,1,1,2,1,1,1,1,1,2]
GROUND = [1,1,0,2,1,2,0.5,1,2,2,1,0.5,2,1,1,1,1,1]
ROCK = [1,0.5,2,1,0.5,1,2,1,0.5,2,1,1,1,1,2,1,1,1]
BUG = [1,0.5,0.5,0.5,1,1,1,0.5,0.5,0.5,1,2,1,2,1,1,2,0.5]
GHOST = [0,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,0.5,1]
STEEL = [1,1,1,1,1,2,1,1,0.5,0.5,0.5,1,0.5,1,2,1,1,2]
FIRE = [1,1,1,1,1,0.5,2,1,2,0.5,0.5,2,1,1,2,0.5,1,1]
WATER = [1,1,1,1,2,2,1,1,1,2,0.5,0.5,1,1,1,0.5,1,1]
GRASS = [1,1,0.5,0.5,2,2,0.5,1,0.5,0.5,2,0.5,1,1,1,0.5,1,1]
ELECTRIC = [1,1,2,1,0,1,1,1,1,1,2,0.5,0.5,1,1,0.5,1,1]
PSYCHIC = [1,2,1,2,1,1,1,1,0.5,1,1,1,1,0.5,1,1,0,1]
ICE = [1,1,2,1,2,2,1,1,0.5,0.5,0.5,2,1,1,0.5,2,1,1]
DRAGON = [1,1,1,1,1,1,1,1,0.5,1,1,1,1,1,1,2,1,0]
DARK = [1,0.5,1,1,1,1,1,2,1,1,1,1,1,2,1,1,0.5,0.5]
FAIRY = [1,2,1,0.5,1,1,1,1,0.5,0.5,1,1,1,1,1,2,2,1]

effectiveness = np.matrix([NORMAL,FIGHTING,FLYING,POISON,GROUND,ROCK,BUG,GHOST,STEEL,FIRE,WATER,GRASS,ELECTRIC,PSYCHIC,ICE,DRAGON,DARK,FAIRY])

typ = {'NORMAL': 0,
       'FIGHTING': 1,
       'FLYING': 2,
       'POISON': 3,
       'GROUND': 4,
       'ROCK': 5,
       'BUG': 6,
       'GHOST': 7,
       'STEEL': 8,
       'FIRE': 9,
       'WATER': 10,
       'GRASS': 11,
       'ELECTRIC': 12,
       'PSYCHIC': 13,
       'ICE': 14,
       'DRAGON': 15,
       'DARK': 16,
       'FAIRY': 17}

def eff(type1,type2):
	return(effectiveness[typ[type1],typ[type2]])

print(typ['FIGHTING'])
print(effectiveness.shape)
print(eff('FIGHTING','DARK')) #prints effectiveness from fighting against dark


#		NOR	FGH	FLY	POI	GRN	ROC	BUG	GHO	STL	FIR	WAT	GRA	ELC	PSY	ICE	DRA	DAK	FAY
#	NOR	1	1	1	1	1	0.5	1	0	0.5	1	1	1	1	1	1	1	1	1
#	FGH	2	1	1	0.5	0.5	2	0.5	0	2	1	1	1	1	0.5	2	1	2	0.5
#	FLY	1	2	1	1	1	0.5	2	1	0.5	1	1	2	0.5	1	1	1	1	1
#	POI	1	1	1	0.5	0.5	0.5	1	0.5	0	1	1	2	1	1	1	1	1	2
#	GRN	1	1	0	2	1	2	0.5	1	2	2	1	0.5	2	1	1	1	1	1
#	ROC	1	0.5	2	1	0.5	1	2	1	0.5	2	1	1	1	1	2	1	1	1
#	BUG	1	0.5	0.5	0.5	1	1	1	0.5	0.5	0.5	1	2	1	2	1	1	2	0.5
#	GHO	0	1	1	1	1	1	1	2	1	1	1	1	1	2	1	1	0.5	1
#	STL	1	1	1	1	1	2	1	1	0.5	0.5	0.5	1	0.5	1	2	1	1	2
#	FIR	1	1	1	1	1	0.5	2	1	2	0.5	0.5	2	1	1	2	0.5	1	1
#	WAT	1	1	1	1	2	2	1	1	1	2	0.5	0.5	1	1	1	0.5	1	1
#	GRA	1	1	0.5	0.5	2	2	0.5	1	0.5	0.5	2	0.5	1	1	1	0.5	1	1
#	ELC	1	1	2	1	0	1	1	1	1	1	2	0.5	0.5	1	1	0.5	1	1
#	PSY	1	2	1	2	1	1	1	1	0.5	1	1	1	1	0.5	1	1	0	1
#	ICE	1	1	2	1	2	2	1	1	0.5	0.5	0.5	2	1	1	0.5	2	1	1
#	DRA	1	1	1	1	1	1	1	1	0.5	1	1	1	1	1	1	2	1	0
#	DAK	1	0.5	1	1	1	1	1	2	1	1	1	1	1	2	1	1	0.5	0.5
#	FAY	1	2	1	0.5	1	1	1	1	0.5	0.5	1	1	1	1	1	2	2	1


#////////////// 2-typed mons //////////////////////
resist_sum = effectiveness.T * effectiveness

best = np.unravel_index(resist_sum.argmin(), resist_sum.shape)
typenames[best[0]], typenames[best[1]]

ncomb=n**2
with open('two_types.txt', 'w') as f:
	for i in range(ncomb):
		best = np.unravel_index(np.argsort(resist_sum,axis=None)[0,i], resist_sum.shape)
		f.write(str(typenames[best[0]]) + ' ' + str(typenames[best[1]]) + ': ' + str(resist_sum[best]) + '\n')
		#print(str(typenames[best[0]]) + ' ' + str(typenames[best[1]]) + ': ' + str(resist_sum[best]))
#//////////////////////////////////////////////////










#////////////// 3-typed mons //////////////////////////////////////////
resist_sum3 = np.zeros((n,n,n))
n=len(typenames)
for x in range(n):
	for y in range(n):
		for z in range(n):
			resist_sum3[x,y,z] = np.sum(np.multiply(np.multiply(effectiveness[:,x],effectiveness[:,y]),effectiveness[:,z]))


#best = np.unravel_index(resist_sum3.argmin(), resist_sum3.shape)
#typenames[best[0]], typenames[best[1]], typenames[best[2]]

#resist_sum3 = np.triu(resist_sum3)
ncomb=n**3
with open('three_types.txt', 'w') as f:
	for i in range(ncomb):
		best = tuple(np.array(np.unravel_index(np.argsort(resist_sum3,axis=None), resist_sum3.shape))[:,i])
		f.write(str(typenames[best[0]]) + ' ' + str(typenames[best[1]]) + ' ' + str(typenames[best[2]]) + ': ' + str(resist_sum3[best]) + '\n')
		#print(str(typenames[best[0]]) + ' ' + str(typenames[best[1]]) + ' ' + str(typenames[best[2]]) + ': ' + str(resist_sum3[best]))
'''
ncomb=n**3
for i in range(ncomb):
	best = tuple(np.array(np.unravel_index(np.argsort(resist_sum3,axis=None), resist_sum3.shape))[:,i])
	if best[0] == typ['WATER'] and best[1] == typ['POISON']:
		print(str(typenames[best[0]]) + ' ' + str(typenames[best[1]]) + ' ' + str(typenames[best[2]]) + ': ' + str(resist_sum3[best]))
'''



#//////////////////////////////////////////////////////////////////////
