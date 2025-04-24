'''
Libraries / Modules Pre Installed:
	- os
	- sys
	- math
	- string

Nytescript Shell and Intepreter, written by @_nnn_ (A.K.A @FlyBoyAce2) in Python 3.12.9, 3.13.2 and 3.13.3	

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

This is an interpreted programming Language made in Python named Nytescript. It has essential functions such as
printing, input, conditional statements, definable functions, while and for loops, and the ability to run files and 
exit the programme. It supports comments in regional currency symbols $, £, #, € and ¥ with a format like Python for single line comments.

Nothing needs to be installed except the 'nytescript.py' file, preferably Python 3.12 and above.

© Copyright @_nnn_ 2025 - 2025
'''

import nytescript
import os, sys, platform

def shell() -> None:
	os.system('clear' if os.name == 'posix' else 'cls')
	# INTEPRETER_LANG = ((sys.version.split(' (')[1]).split(') ['))[0]
	INTEPRETER_LANG = sys.version.split(' [')[0]
	BOOT_INFO = f'Nytescript {nytescript.VERSION} [Python {INTEPRETER_LANG}] on {platform.system() if platform.system() != 'Darwin' else 'Darwin (MacOS)'}'

	print(BOOT_INFO)
	while True:
		text = input("❯ ")
		if text.strip() == "": continue
		result, error = nytescript.run('<stdin>', text)

		if error:
			print(error.as_string())
		elif result:
			if len(result.elements) == 1:
				if repr(result.elements[0]) != 'NoneType':
					print(repr(result.elements[0]))
				else:
					...
			else:
				print(repr(result))

def intepreter(file) -> None:
	result, error = nytescript.run('<program>', f'run(\'{file}\')')

	if error:
		print(error.as_string())
	elif result:
		...

def cli() -> None:
	if len(sys.argv) == 1:
		shell()
	elif len(sys.argv) == 2:
		intepreter(sys.argv[1])
	else:
		raise Exception(f"Too many arguments were passed into Nytescript CLI")
	
if __name__ == '__main__':
	cli()
