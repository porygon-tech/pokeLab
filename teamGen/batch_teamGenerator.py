
import teamGen
#teamGen.get_years()
#teamGen.get_metas('2022-12/') #'gen8uu-1500.json', 'gen8uu-1630.json', 'gen8uu-1760.json'

#db = teamGen.get_meta_json('gen8ou-0.json', year='2022-02/')
db = teamGen.get_meta_json('gen8ou-0.json', year='2022-12/')

top = teamGen.filterbest(db,competition_level = 0.005)
import os

os.system('mkdir teams')

for i in range(10):
	f = open('teams/team_' + str(i) + '.txt', "w")
	f.write(teamGen.makeTeam(top))
	f.close()

