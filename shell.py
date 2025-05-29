'''
Nytescript Esolang, written by @_nnn_ (A.K.A @FlyBoyAce2) in Python 3.12.9 and 3.13.2 and 3.13.3	

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

This is an esoteric interpreted programming Language made in Python named Nytescript. It has essential functions such as
printing, input, conditional statements, definable functions, while and for loops, switch and try-except statements, and the ability to run files and 
exit the programme.

Nothing needs to be installed except the ```nytescript.py``` and ```shell.py``` file, preferably Python 3.12 and above.

© Copyright @_nnn_ 2025 - 2025
'''

import nytescript
import os, sys, platform
from functools import cache

if sys.platform != 'win32':
	try:
		import readline
		history_file = os.path.join(os.path.expanduser('~'), '.nytescript_history')
		try:
			readline.read_history_file(history_file)
		except FileNotFoundError:
			pass
		except PermissionError:
			pass

		import atexit
		atexit.register(readline.write_history_file, history_file)

	except:
		pass

@cache
def shell() -> None:
	os.system('clear' if os.name == 'posix' else 'cls')
	INTEPRETER_LANG = sys.version.split(' [')[0]
	BOOT_INFO = f'Nytescript {nytescript.VERSION} [Python {INTEPRETER_LANG}] on {platform.system() if platform.system() != "Darwin" else "Darwin (MacOS)"}'

	print(BOOT_INFO)
	while True:
		try:
			text = input("❯ ")
		except EOFError:
			break
		except KeyboardInterrupt:
			print("^C")
			continue

		if text.strip() == "": continue
		result, error = nytescript.run('<stdin>', text)
		if error:
			print(error.as_string())
		elif result:
			if len(result.elements) == 1:
				if repr(result.elements[0]) != 'None':
					print(repr(result.elements[0]))
				else:
					...
			else:
				print(repr(result))

@cache
def intepreter(fn) -> None:
	try:
		with open(fn, "r") as f:
			script = f.read()
			if not script.strip() == '':
				_, error = nytescript.run('<program>', script)
				if error:
					print(error.as_string())
	except FileNotFoundError:
		print(f"Failed to load script \"{fn}\": File not found")
	except PermissionError:
		print(f"Failed to open script \"{fn}\": Lacking Permissions")
	except Exception as e:
		print(f"Failed to load script \"{fn}\": {e}")	

def cli() -> None:
	if len(sys.argv) == 1:
		shell()
	elif len(sys.argv) >= 2:
		rt = ' '.join(sys.argv[1:])
		intepreter(rt)
	else:
		raise Exception(f"Nytescript CLI Failed")
	
if __name__ == '__main__':
	cli()