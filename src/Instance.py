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