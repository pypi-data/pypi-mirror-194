import random, requests, sys
from os.path import abspath, join, dirname

full_path = lambda filename: abspath(join(dirname(__file__), filename))

file = {
    'malename': full_path('malename.txt'),
    'femalename': full_path('femalename.txt'),
    'maletitle': full_path('maletitle.txt'),
	'femaletitle': full_path('femaletitle.txt'),
	'pyver': full_path('pyversion.txt'),
}

space =" "

with open(file["malename"], encoding="utf-8") as mn:
    msufix = mn.read().splitlines()

with open(file["femalename"], encoding="utf-8") as fn:
    fsufix = fn.read().splitlines()

with open(file["maletitle"], encoding="utf-8") as mt:
    mprefix = mt.read().splitlines()

with open(file["femaletitle"], encoding="utf-8") as fmt:
    fprefix = fmt.read().splitlines()

allname=fsufix+msufix
alltitle=mprefix+fprefix

def randname():
	return random.choice(allname)+space+random.choice(alltitle)
	
def female():
	return random.choice(fsufix)+space+random.choice(fprefix)
	
def male():
	return random.choice(msufix)+space+random.choice(mprefix)

def pypicheck():
	try :
		oldpv=open(file["pyver"],"r")
		oldp = oldpv.read()
		newp = requests.get("https://raw.githubusercontent.com/techux/getindianname/main/getindianname/pypiversion").text
		if str(oldp)==str(newp):
			pass
		else:
			print("Update Available on Pypi\n\nPlease Update it.")
	except:
		pass

pypicheck()

def help():
	print('''
	\t \ngetindianname — Generate Indian Name\n\n
Import on your project\n
\t import getindianname as name
\t print(name.male())
\t print(name.female())
\t print(name.randname())
\n\nUse as Command Prompt Utility\n
\t $ name   —   generate random name
\t $ name male   —   generate male name
\t $ name female   —   generate female name
\t $ name random   —   generate random name\n\n
Latest Documentation : https://github.com/TechUX/getindianname\n
	''')

def main():
	try :
		if sys.argv[1].lower() == "male" :
			print(male())
		elif sys.argv[1].lower() == "female":
			print(female())
		elif sys.argv[1].lower() == "help" :
			help()
		elif sys.argv[0] :
			print(randname())
		else:
			print(randname())
	except:
		print(randname())

if __name__ == "__main__":
    main()