'''
Nytescript Shell and Interpreter, written by @0xnCubed in Python 3.12, 3.13 and 3.14.

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

© Copyright @0xnCubed 2025 - 2026
'''

import Data
import Runtime
from functools import cache

if Data.sys.platform != 'win32':
	try:
		import readline
		history_file = Data.os.path.join(Data.os.path.expanduser('~'), '.nytescript_history')
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
	INTEPRETER_LANG = Data.sys.version.split(' [')[0]
	BOOT_INFO = f'Nytescript {Data.VERSION} [Python {INTEPRETER_LANG}] on {Data.platform.system() if Data.platform.system() != "Darwin" else "Darwin (MacOS)"}\nType "license" or "help" for more information and "exit" to quit'

	print(BOOT_INFO)
	while True:
		try:
			text = input("❯ ")
		except EOFError:
			print()
			break
		except KeyboardInterrupt:
			print("^C")
			continue
		except Exception as e:
			if Data.MODE == 0:
				print(f'[SHELL ERROR]: {e}')
			continue

		if text.strip() == "": continue
		result, error = Runtime.run('<dev>' if Data.MODE == 0 else '<stdin>', text)
		if error:
			print(error.as_string())
		elif result:
			if len(result.elements) == 1:
				try:
					if result.elements[0].elements[0] == 'None':
						print(repr(result.elements.pop(0)))
					elif len(result.elements[0]) != 0:
						print(repr(result.elements[0]))
					continue
				except:
					...
				if repr(result.elements[0]) != 'None':
					print(repr(result.elements[0]))
			else:
				for i in result.elements:
					if repr(i) != 'None':
						print(repr(i))

@cache
def intepreter(fn) -> None:
	try:
		with open(fn, "r") as f:
			script = f.read()
			if not script.strip() == '':
				_, error = Runtime.run('<dev>' if Data.MODE == 0 else '<program>', script)
				if error:
					print(error.as_string())
				del _
	except FileNotFoundError:
		print(f"Failed to load script \"{fn}\": File not found")
	except PermissionError:
		print(f"Failed to open script \"{fn}\": Lacking Permissions")
	except Exception as e:
		print(f"Failed to load script \"{fn}\": {e}")	

def cli() -> None:
	if len(Data.sys.argv) == 1:
		shell()
	elif len(Data.sys.argv) >= 2:
		if Data.sys.argv[1] != ('--version' or '-v'):
			intepreter(' '.join(Data.sys.argv[1:]))
		else:
			print(f'Nytescript {Data.VERSION}')
		
	else:
		raise Exception(f"Nytescript CLI Failed")
	
if __name__ == '__main__':
	cli()