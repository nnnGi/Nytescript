'''
Nytescript Official Shell, written by @0xnCubed in Python 3.14.

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan
'''
import Data, Runtime
from Instance import ForeColours

class Hooks:
	def __init__(self) -> None:
		self.INTEPRETER_LANG = Data.sys.version.split(' [')[0]
		self.PLATFORM = Data.platform.system() if Data.platform.system() != "Darwin" else "Darwin (MacOS)"
		self.BOOT_INFO1 = f'Nytescript {Data.VERSION} [Python {self.INTEPRETER_LANG}] on {self.PLATFORM}'
		self.BOOT_INFO2 = 'Type "license" or "help" for more information and "exit" to quit'
	
	@Data.cache
	def print_as_string(self, text) -> None:
		if len(text.elements) == 1:
			if isinstance(text.elements[0], Runtime.List):
				self.print_as_string(text.elements[0])
			elif repr(text.elements[0]) != 'None' and text.elements[0] != Runtime.NoneType.none:
				print(repr(text.elements[0]))
		else:
			for i in text.elements:
				if repr(i) != 'None':
					self.print_as_string(Runtime.List([i]))
					
		return None

@Data.cache
def shell(inert) -> None:
	if Data.sys.platform != 'win32':
		try:
			import readline
			history_file = Data.os.path.join(Data.os.path.expanduser('~'), '.nytescript_history')
			try:
				readline.read_history_file(history_file)
			except:
				...
				
			import atexit
			atexit.register(readline.write_history_file, history_file)

		except:
			...

	print(f'{ForeColours.BLUE}{inert.BOOT_INFO1}\n{ForeColours.RESET}{inert.BOOT_INFO2}')
	while True:
		try:
			text = input(f"{ForeColours.GREEN}❯ {ForeColours.RESET}")
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
			print(f'{ForeColours.BRED}{error.as_string()}{ForeColours.RESET}')
		elif result:
			inert.print_as_string(result)
			
	return None

@Data.cache
def intepreter(fn) -> None:
	try:
		with open(fn, "r") as f:
			script = f.read()
			if not script.strip() == '':
				_, error = Runtime.run('<dev>' if Data.MODE == 0 else '<program>', script)
				if error:
					print(f'{ForeColours.RED}{error.as_string()}{ForeColours.RESET}')
	except FileNotFoundError:
		print(f"Failed to load script \"{fn}\": No such file or directory")
	except PermissionError:
		print(f"Failed to open script \"{fn}\": Lacking Permissions")
	except Exception as e:
		print(f"Failed to load script \"{fn}\": {e}")	

def cli() -> None:
	if len(Data.sys.argv) == 1:
		shell(Hooks())
	elif len(Data.sys.argv) >= 2:
		if Data.sys.argv[1][0] == '-':
			if Data.sys.argv[1] in ('--version', '-v'):
				print(f'{Data.VERSION}')
			elif Data.sys.argv[1] in ('--interpreter', '-i'):
				print(f'Nytescript {Data.VERSION} running on Python {Data.sys.version.split(' [')[0]}')
		else:
			intepreter(' '.join(Data.sys.argv[1:]))
	else:
		raise Exception(f"Nytescript CLI Failed")
	
if __name__ == '__main__':
	cli()