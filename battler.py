from mechanize import Browser as BR
import cookielib
#https://www.pythonforbeginners.com/cheatsheet/python-mechanize-cheat-sheet
br = BR()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#br.open("https://pokemonshowdown.com/damagecalc/")
br.open("https://www.google.es/")
#br.open("https://www.ncbi.nlm.nih.gov/nuccore")


#br.open("https://play.pokemonshowdown.com/")
'''
for form in br.forms():
	print("\nForm name: " + form.name)
	print(form)
'''
br.select_form("f")
html = br.read()
print(html)
'''
for control in br.form.controls:
    #print(control)
    #print("type=%s, name=%s" % (control.type, control.name))
    print("type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
'''
#control = br.form.find_control("q")

br['q'] = 'foo'

br.submit()


content = resp.get_data()
print(content)











'''
br.select_form("EntrezForm")


for control in br.form.controls:
    #print(control)
    print("type=%s, name=%s" % (control.type, control.name))
    #print("type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))

control = br.form.find_control("term")

'''