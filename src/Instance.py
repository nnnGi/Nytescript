#######################################
# HELPER FUNCTIONS
#######################################

def isclass(obj: any) -> bool:
	return isinstance(obj, type)

def isfunction(obj: any) -> bool:
	return isinstance(obj, type(lambda: None))

def ismethod(obj: any) -> bool:
	return callable(obj)

def isnum(obj: any) -> bool:
	return isinstance(obj, (int, float))

def isbool(obj: any) -> bool:
	return isinstance(obj, bool)

def isstr(obj: any) -> bool:
	return isinstance(obj, str)

def islist(obj: any) -> bool:
	return isinstance(obj, list)

def isnone(obj: any) -> bool:
	return obj is None

def isobject(obj: any) -> bool:
	return isinstance(obj, object)

#######################################
# TEXT FORMATTING CLASSES
#######################################

class ForeColours:
	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	BBLACK = '\033[90m'
	BRED = '\033[91m'
	BGREEN = '\033[92m'
	BYELLOW = '\033[93m'
	BBLUE = '\033[94m'
	BMAGENTA = '\033[95m'
	BCYAN = '\033[96m'
	BWHITE = '\033[97m'
	RESET = '\033[0m'

class BackColours:
	BLACK = '\033[40m'
	RED = '\033[41m'
	GREEN = '\033[42m'
	YELLOW = '\033[43m'
	BLUE = '\033[44m'
	MAGENTA = '\033[45m'
	CYAN = '\033[46m'
	WHITE = '\033[47m'
	BBLACK = '\033[100m'
	BRED = '\033[101m'
	BGREEN = '\033[102m'
	BYELLOW = '\033[103m'
	BBLUE = '\033[104m'
	BMAGENTA = '\033[105m'
	BCYAN = '\033[106m'
	BWHITE = '\033[107m'
	RESET = '\033[0m'

class Formatting:
	BOLD = '\x1b[1m'
	DIM = '\x1b[2m'
	ITALIC = '\x1b[3m'
	UNDERLINE = '\x1b[4m'
	BLINK = '\x1b[5m'
	STRIKE = '\x1b[9m'
	COLOUR256 = '\x1b=19h'
	RESET = '\x1b[0m'