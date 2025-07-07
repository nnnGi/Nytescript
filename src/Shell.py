'''
Nytescript Shell and Interpreter, written by @_nnn_ in Python 3.12.9, 3.13.2 and 3.13.3

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

© Copyright @_nnn_ 2025 - 2025
'''

import ConstantData
import Runtime
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
	BOOT_INFO = f'Nytescript {ConstantData.VERSION} [Python {INTEPRETER_LANG}] on {platform.system() if platform.system() != "Darwin" else "Darwin (MacOS)"}'

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
		result, error = Runtime.run('<stdin>', text)
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
				_, error = Runtime.run('<program>', script)
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