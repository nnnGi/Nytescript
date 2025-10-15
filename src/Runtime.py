from Errors import RTError, RecursiveError, KeyboardInterrupted
from Parser import Parser, RTResult
from Lexer import Lexer, Token, Position, KEYWORDS, SYMBOL_TABLE
from Tokens import *
from Helper import Help
from Data import FILE_EXTENSION, STDLIB, os, sys, importlib

from inspect import isclass 

#######################################
# VALUES
#######################################

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		return None, self.illegal_operation(other)

	def subbed_by(self, other):
		return None, self.illegal_operation(other)

	def multed_by(self, other):
		return None, self.illegal_operation(other)

	def dived_by(self, other):
		return None, self.illegal_operation(other)

	def powed_by(self, other):
		return None, self.illegal_operation(other)

	def percent_by(self, other):
		return None, self.illegal_operation(other)

	def fdiv_by(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_eq(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_ne(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lte(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gte(self, other):
		return None, self.illegal_operation(other)

	def anded_by(self, other):
		return None, self.illegal_operation(other)

	def ored_by(self, other):
		return None, self.illegal_operation(other)

	def notted(self, other):
		return None, self.illegal_operation(other)

	def execute(self, args):
		return RTResult().failure(self.illegal_operation())

	def get_member(self, name):
		return None, self.illegal_operation()

	def copy(self):
		raise Exception('No copy method defined')

	def is_true(self):
		return False

	def illegal_operation(self, other=None):
		if not other: other = self
		return RTError(
			self.pos_start, other.pos_end,
			'Illegal operation',
			self.context, "AttributeError"
		)

class NoneType(Value):
	def __init__(self):
		super().__init__()

	def copy(self):
		copy = NoneType()
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return 'None'

	def __repr__(self):
		return 'None'

NoneType.none = NoneType()

class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Division by Zero',
					self.context, "Math Error"
				)

			return Number(self.value / other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def powed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def fdiv_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Division by Zero',
					self.context
				)
			return Number(self.value // other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def percent_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Modulo by Zero',
					self.context
				)
			return Number(self.value % other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gt(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lte(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gte(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def anded_by(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def ored_by(self, other):
		if isinstance(other, Number):
			return Bool(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def notted(self):
		return Bool(1 if self.value == 0 else 0).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def is_true(self):
		return self.value != 0

	def __str__(self):
		if isinstance(self.value, float):
			return f"{self.value:.10f}".rstrip('0').rstrip('.') or '0'
		return str(self.value)

	def __repr__(self):
		return str(self.value)


Number.null = Number(0)

class Bool(Number):
	def __init__(self, value):
		super().__init__(value)
		self.value = value
		if self.value not in [0, 1]:
			self.value = 0
	
	def copy(self):
		copy = Bool(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __str__(self):
		return 'True' if self.value == 1 else 'False'

	def __repr__(self):
		return 'True' if self.value == 1 else 'False'

Bool.true = Bool(1)
Bool.false = Bool(0)

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			if not isinstance(other.value, int):
				return None, RTError(
					other.pos_start, other.pos_end,
					'String multiplication requires an integer',
					self.context
				)
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			if not isinstance(other.value, int):
				return None, RTError(
					other.pos_start, other.pos_end,
					'String indexing requires an integer',
					self.context
				)
			try:
				return String(self.value[other.value]).set_context(self.context), None
			except:
				return None, RTError(
					other.pos_start, other.pos_end,
					'String index out of bounds',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def powed_by(self, other):
		if isinstance(other, Number):
			if not isinstance(other.value, int) or other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'String slicing step requires a non-zero integer',
					self.context
				)
			try:
				return String(self.value[::other.value]).set_context(self.context), None
			except Exception:
				return None, RTError(
					other.pos_start, other.pos_end,
					'String slicing with step failed',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, String):
			return Bool(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, String):
			return Bool(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return self.value

	def __repr__(self):
		return f'"{self.value.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")}"'

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements

	def added_to(self, other):
		new_list = self.copy()
		new_list.elements.append(other)
		return new_list, None

	def subbed_by(self, other):
		if isinstance(other, Number):
			if not isinstance(other.value, int):
				return None, RTError(
					other.pos_start, other.pos_end,
					'List pop requires an integer index',
					self.context
				)
			new_list = self.copy()
			try:
				new_list.elements.pop(other.value)
				return new_list, None
			except IndexError:
				return None, RTError(
					other.pos_start, other.pos_end,
					'List index out of bounds for pop',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, List):
			new_list = self.copy()
			new_list.elements.extend(other.elements)
			return new_list, None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			if not isinstance(other.value, int):
				return None, RTError(
					other.pos_start, other.pos_end,
					'List indexing requires an integer',
					self.context
				)
			try:
				return self.elements[other.value], None
			except IndexError:
				return None, RTError(
					other.pos_start, other.pos_end,
					'List index out of bounds',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def powed_by(self, other):
		if isinstance(other, Number):
			if not isinstance(other.value, int) or other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'List slicing step requires a non-zero integer',
					self.context
				)
			try:
				return List(self.elements[::other.value]).set_context(self.context), None
			except:
				return None, RTError(
					other.pos_start, other.pos_end,
					'List slicing with step failed',
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, List):
			if len(self.elements) != len(other.elements):
				return Bool.false.set_context(self.context), None
			for i in range(len(self.elements)):
				comparison_result, error = self.elements[i].get_comparison_eq(other.elements[i])
				if error: return None, error
				if not comparison_result.is_true():
					return Bool.false.set_context(self.context), None
			return Bool.true.set_context(self.context), None
		else:
			return Bool.false.set_context(self.context), None

	def get_comparison_ne(self, other):
		comparison_result, error = self.get_comparison_eq(other)
		if error: return None, error
		return Bool(1 - comparison_result.value).set_context(self.context), None

	def copy(self):
		copy = List(self.elements)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def is_true(self):
		return len(self.elements) > 0

	def __str__(self):
		return ", ".join([str(x) for x in self.elements])

	def __repr__(self):
		return f'[{", ".join([repr(x) for x in self.elements])}]'

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or "<anonymous>"

	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)

		parent_symbol_table = new_context.parent.symbol_table if new_context.parent else None

		new_context.symbol_table = SymbolTable(parent_symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RTResult()

		if len(args) == 0:
			return res.success(NoneType.none)

		if len(args) > len(arg_names):
			return res.failure(RTError(
				self.pos_start, self.pos_end,
				f"{len(args) - len(arg_names)} too many args passed into {self}",
				self.context
			))

		if len(args) < len(arg_names):
			return res.failure(RTError(
				self.pos_start, self.pos_end,
				f"{len(arg_names) - len(args)} too few args passed into {self}",
				self.context
			))

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RTResult()
		res.register(self.check_args(arg_names, args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return

	def bind_to_instance(self, instance):
		new_method = self.copy()
		new_method.instance = instance
		return new_method

	def execute(self, args):
		res = RTResult()
		interpreter = Interpreter()
		exec_ctx = self.generate_new_context()

		res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		if res.should_return(): return res

		body_execution_result = interpreter.visit(self.body_node, exec_ctx)
		
		res.register(body_execution_result) 

		if res.should_return() and res.func_return_value is None:
			return res

		final_return_value = NoneType.none

		if self.should_auto_return:
			final_return_value = body_execution_result.value 
		elif res.func_return_value is not None:
			final_return_value = res.func_return_value
		
		return res.success(final_return_value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<Defined Function {self.name}>"

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if res.should_return(): return res

		return_value = res.register(method(exec_ctx))
		if res.should_return(): return res

		return res.success(return_value)


	def no_visit_method(self, node, context):
		raise Exception(f'No execute_{self.name} method defined')

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<nytescript {self.name}>"

	#####################################

	def execute_print(self, exec_ctx):
		value = exec_ctx.symbol_table.get('value')
		print(f'{value}')
		return RTResult().success(NoneType.none)
	execute_print.arg_names = ['value']

	def execute_print_ret(self, exec_ctx):
		return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
	execute_print_ret.arg_names = ['value']

	def execute_input(self, exec_ctx):
		text = input()
		return RTResult().success(String(text))
	execute_input.arg_names = []

	def execute_input_char(self, exec_ctx):
		while True:
			char = input()
			if len(char) == 1:
				break
			else:
				print(f"'{char}' must be a single character. Try again!")
		return RTResult().success(String(char))
	execute_input_char.arg_names = []

	def execute_input_int(self, exec_ctx):
		while True:
			text = input()
			try:
				number = int(text)
				break
			except ValueError:
				print(f"'{text}' must be an integer. Try again!")
		return RTResult().success(Number(number))
	execute_input_int.arg_names = []

	def execute_clear(self, exec_ctx):
		os.system('cls' if os.name == 'nt' else 'clear')
		return RTResult().success(NoneType.none)
	execute_clear.arg_names = []

	def execute_exit(self, exec_ctx):
		exit_code = exec_ctx.symbol_table.get('value')
		if isinstance(exit_code, Number):
			if exit_code.value in range(0, 256):
				exit(exit_code.value)
		return RTResult().failure(RTError(
			self.pos_start, self.pos_end,
			f"Exit Code: {exit_code} is not a valid error code.",
			exec_ctx
		))
	execute_exit.arg_names = ['value']

	def execute_Number(self, exec_ctx):
		data_value = exec_ctx.symbol_table.get('value')
		try:
			value_str = str(data_value)
			if '.' in value_str:
				result = float(value_str)
			else:
				result = int(value_str)
		except (ValueError, TypeError) as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Cannot convert value to Number: {e}",
				exec_ctx
			))
		return RTResult().success(Number(result))
	execute_Number.arg_names = ['value']

	def execute_Bool(self, exec_ctx):
		data_value = exec_ctx.symbol_table.get('value')
		try:
			result = int(data_value.value)
		except (ValueError, TypeError) as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Cannot convert value to Boolean: {e}",
				exec_ctx
			))
		return RTResult().success(Bool(result))
	execute_Bool.arg_names = ['value']

	def execute_String(self, exec_ctx):
		value = exec_ctx.symbol_table.get('value')
		try:
			result_str = str(value)
		except Exception as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Cannot convert value to String: {e}",
				exec_ctx
			))
		return RTResult().success(String(result_str))
	execute_String.arg_names = ['value']

	def execute_List(self, exec_ctx):
		value = exec_ctx.symbol_table.get('value')
		if isinstance(value, List):
			return RTResult().success(value.copy())
		try:
			if hasattr(value, 'value') and isinstance(value.value, (list, tuple, str)):
				elements = [elem if isinstance(elem, Value) else String(str(elem)) for elem in list(value.value)]
				return RTResult().success(List(elements))
			elif isinstance(value, (list, tuple, str)):
				elements = [elem if isinstance(elem, Value) else String(str(elem)) for elem in list(value)]
				return RTResult().success(List(elements))
			else:
				return RTResult().failure(RTError(
					self.pos_start, self.pos_end,
					f"Cannot convert type '{type(value).__name__}' to List",
					exec_ctx
				))
		except Exception as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Failed to convert value to List: {e}",
				exec_ctx
			))
	execute_List.arg_names = ['value']

	def execute_strcon(self, exec_ctx):
		list_value = exec_ctx.symbol_table.get("list")
		if not isinstance(list_value, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"strcon argument must be a List",
				exec_ctx
			))
		elements = list_value.elements
		try:
			string_elements = [str(item) for item in elements]
			return RTResult().success(String(''.join(string_elements)))
		except Exception as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Failed to concatenate list elements to String: {e}",
				exec_ctx
			))
	execute_strcon.arg_names = ['list']

	def execute_is_in(self, exec_ctx):
		iterable_value = exec_ctx.symbol_table.get("list")
		item_value = exec_ctx.symbol_table.get("value")

		if isinstance(iterable_value, String):
			if str(item_value) in iterable_value.value:
				return RTResult().success(Bool.true)
			return RTResult().success(Bool.false)

		elif isinstance(iterable_value, List):
			for element in iterable_value.elements:
				comparison_result, error = element.get_comparison_eq(item_value)
				if error: return RTResult().failure(error)
				if comparison_result.is_true():
					return RTResult().success(Bool.true)
			return RTResult().success(Bool.false)

		else:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"First argument to is_in must be an iterable (String or List), not '{type(iterable_value).__name__}'",
				exec_ctx
			))
	execute_is_in.arg_names = ["list", "value"]

	def execute_is_num(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
		return RTResult().success(Bool.true if is_number else Bool.false)
	execute_is_num.arg_names = ["value"]

	def execute_is_string(self, exec_ctx):
		is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
		return RTResult().success(Bool.true if is_string else Bool.false)
	execute_is_string.arg_names = ["value"]

	def execute_is_list(self, exec_ctx):
		is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
		return RTResult().success(Bool.true if is_list else Bool.false)
	execute_is_list.arg_names = ["value"]

	def execute_is_function(self, exec_ctx):
		is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
		return RTResult().success(Bool.true if is_function else Bool.false)
	execute_is_function.arg_names = ["value"]

	def execute_sorted(self, exec_ctx):
		list_value = exec_ctx.symbol_table.get("list")
		reverse_value = exec_ctx.symbol_table.get("value")

		if not isinstance(list_value, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument to sorted must be a list",
				exec_ctx
			))
		if not isinstance(reverse_value, Number):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Second argument to sorted must be a Number (boolean)",
				exec_ctx
			))

		elements = list_value.elements
		reverse = bool(reverse_value.value)

		def sort_key(item):
			if isinstance(item, (Number, String)):
				return item.value
			raise TypeError(f"Cannot sort list containing type '{type(item).__name__}'")

		try:
			sorted_elements = sorted(elements, key=sort_key, reverse=reverse)
			return RTResult().success(List([elem.copy() for elem in sorted_elements]).set_context(exec_ctx).set_pos(list_value.pos_start, list_value.pos_end))

		except TypeError as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Sorting failed: {e}",
				exec_ctx
			))
		except Exception as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Sorting failed with error: {e}",
				exec_ctx
			))
	execute_sorted.arg_names = ["list", "value"]

	def execute_append(self, exec_ctx):
		list_value = exec_ctx.symbol_table.get("list")
		value_to_append = exec_ctx.symbol_table.get("value")

		if not isinstance(list_value, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument to append must be a list",
				exec_ctx
			))

		list_value.elements.append(value_to_append.copy().set_context(list_value.context))
		return RTResult().success(NoneType.none)
	execute_append.arg_names = ["list", "value"]

	def execute_pop(self, exec_ctx):
		list_value = exec_ctx.symbol_table.get("list")
		index_value = exec_ctx.symbol_table.get("index")

		if not isinstance(list_value, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument to pop must be a list",
				exec_ctx
			))

		if not isinstance(index_value, Number):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Second argument to pop must be a number (integer index)",
				exec_ctx
			))

		if not isinstance(index_value.value, int):
			return RTResult().failure(RTError(
				index_value.pos_start, index_value.pos_end,
				"List pop index must be an integer",
				exec_ctx
			))

		try:
			element = list_value.elements.pop(index_value.value)
			return RTResult().success(element.copy().set_pos(list_value.pos_start, list_value.pos_end).set_context(exec_ctx))
		except IndexError:
			return RTResult().failure(RTError(
				index_value.pos_start, index_value.pos_end,
				'List index out of bounds for pop',
				exec_ctx
			))
		except Exception as e:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Pop failed with error: {e}",
				exec_ctx
			))
	execute_pop.arg_names = ["list", "index"]

	def execute_extend(self, exec_ctx):
		listA_value = exec_ctx.symbol_table.get("listA")
		listB_value = exec_ctx.symbol_table.get("listB")

		if not isinstance(listA_value, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument to extend must be a list",
				exec_ctx
			))

		if not isinstance(listB_value, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Second argument to extend must be a list",
				exec_ctx
			))

		listA_value.elements.extend([elem.copy().set_context(listA_value.context) for elem in listB_value.elements])
		return RTResult().success(NoneType.none)
	execute_extend.arg_names = ["listA", "listB"]

	def execute_len(self, exec_ctx):
		value = exec_ctx.symbol_table.get("list")

		if isinstance(value, List):
			return RTResult().success(Number(len(value.elements)))
		elif isinstance(value, String):
			return RTResult().success(Number(len(value.value)))
		else:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"Argument to len must be a list or string, not '{type(value).__name__}'",
				exec_ctx
			))
	execute_len.arg_names = ["list"]

	def execute_run(self, exec_ctx):
		fn_value = exec_ctx.symbol_table.get("fn")

		if not isinstance(fn_value, String):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Argument to run must be a string (filename)",
				exec_ctx
			))

		fn = fn_value.value
		if not fn.endswith(FILE_EXTENSION):
			return RTResult().failure(RTError(
				fn_value.pos_start, fn_value.pos_end,
				f"File Extension should be {FILE_EXTENSION}",
				exec_ctx
			))

		try:
			with open(fn, "r") as f:
				script = f.read()
				if script.strip() == '':
					return RTResult().success(NoneType.none)
		except FileNotFoundError:
			return RTResult().failure(RTError(
				fn_value.pos_start, fn_value.pos_end,
				f"Failed to load script \"{fn}\": File not found",
				exec_ctx
			))
		except Exception as e:
			return RTResult().failure(RTError(
				fn_value.pos_start, fn_value.pos_end,
				f"Failed to load script \"{fn}\": {e}",
				exec_ctx
			))

		module_result_value, module_error = run(fn, script, context=exec_ctx, new_context=True)

		if module_error:
			return RTResult().failure(RTError(
				fn_value.pos_start, fn_value.pos_end,
				f"Error executing script \"{fn}\":\n{module_error.as_string()}",
				exec_ctx
			))

		return RTResult().success(module_result_value if module_result_value is not None else NoneType.none)

	execute_run.arg_names = ["fn"]

class BuiltInMethod(BaseFunction):
	def __init__(self, name, py_func):
		super().__init__(name)
		self.py_func = py_func

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		# 1. Unwrap arguments from Nytescript Values to Python types
		py_args = []
		for arg in args:
			if isinstance(arg, Number):
				py_args.append(arg.value)
			elif isinstance(arg, String):
				py_args.append(arg.value)
			elif isinstance(arg, List):
				# Note: This unwraps recursively, which might not be what you want for all functions.
				# For a function like random.choice, you need the List object itself.
				# This simple version works for math functions.
				py_args.append([elem.value for elem in arg.elements])
			elif isinstance(arg, NoneType):
				py_args.append(None)
			else:
				# If a function needs the raw Nytescript object (e.g., random.choice),
				# you would handle it here by passing `arg` directly.
				py_args.append(arg)


		# 2. Call the actual Python function
		try:
			return_value = self.py_func(*py_args)
		except Exception as e:
			return res.failure(RTError(
				self.pos_start, self.pos_end,
				f"'{self.name}': {e}",
				exec_ctx, error_title="Standard Library Error"
			))

		# 3. Wrap the Python return value back into a Nytescript Value
		wrapped_value = None
		if isinstance(return_value, (int, float)):
			wrapped_value = Number(return_value)
		elif isinstance(return_value, str):
			wrapped_value = String(return_value)
		elif isinstance(return_value, bool):
			wrapped_value = Bool.true if return_value else Bool.false
		elif isinstance(return_value, list):
			wrapped_value = List([Number(item) for item in return_value]) # Simple wrapping
		elif return_value is None:
			wrapped_value = NoneType.none
		else:
			# Fallback for unexpected types
			wrapped_value = String(str(return_value))

		return res.success(wrapped_value.set_context(exec_ctx).set_pos(self.pos_start, self.pos_end))

	def copy(self):
		copy = BuiltInMethod(self.name, self.py_func)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<Stdlib {self.name}>"

# In Runtime.py, after the 'class List(Value): ...' definition

class PyObject(Value):
	"""Wrapper for Python object instances (like the File object)."""
	def __init__(self, py_object):
		super().__init__()
		self.py_object = py_object # The actual Python object instance

	def copy(self):
		copy = PyObject(self.py_object)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return repr(self.py_object)

	# Utility function to convert Python types back to interpreter Value types
	def wrap_py_value(self, py_value):
		"""Converts a raw Python value to the appropriate Nytescript Value."""
		if py_value is None:
			return NoneType.none
		if isinstance(py_value, (int, float)):
			return Number(py_value)
		if isinstance(py_value, str):
			return String(py_value)
		if isinstance(py_value, list):
			return List([self.wrap_py_value(e) for e in py_value])
		if isclass(py_value):
			return PyClass(py_value)
		if callable(py_value):
			return BuiltInMethod(py_value.__name__, py_value)
		
		# Default wrapper for other complex Python objects
		return PyObject(py_value)

	def get_member(self, member_name):
		res = RTResult()

		member_name = member_name.value if hasattr(member_name, 'value') else str(member_name)

		if not hasattr(self.py_object, member_name):
			return None, res.failure(RTError(
				self.pos_start, self.pos_end,
				f"Python object '{type(self.py_object).__name__}' has no member '{member_name}'",
				self.context, "AttributeError"
			))

		py_member = getattr(self.py_object, member_name)

		# If the member is callable (a method), wrap it in PyMethod
		if callable(py_member) and not isclass(py_member):
			method_wrapper = PyMethod(py_member, self)
			return method_wrapper.set_context(self.context).set_pos(self.pos_start, self.pos_end), None
		
		# If it's a data attribute, wrap its value
		return self.wrap_py_value(py_member).set_context(self.context).set_pos(self.pos_start, self.pos_end), None

class PyClass(Value):
	"""Wrapper for Python classes."""
	def __init__(self, py_class):
		super().__init__()
		self.py_class = py_class
		self.name = py_class.__name__
		
	def execute(self, args):
		"""Handles the constructor call."""
		res = RTResult()
		
		# Unwrap all arguments for the constructor call
		unwrapped_args = [arg.py_object if isinstance(arg, PyObject) else arg.value 
						  for arg in args if hasattr(arg, 'value') or isinstance(arg, PyObject)]

		try:
			# Call the Python class constructor
			py_instance = self.py_class(*unwrapped_args)
			
			# Wrap the new Python instance in PyObject
			py_object = PyObject(py_instance).set_context(self.context).set_pos(self.pos_start, self.pos_end)
			return res.success(py_object)

		except Exception as e:
			return res.failure(RTError(self.pos_start, self.pos_end, f"Python Constructor Error: {str(e)}", self.context))
		
	def copy(self):
		copy = PyClass(self.py_class)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return f'<PyClass {self.name}>'

class PyMethod(Value):
	"""Wrapper for Python methods bound to a PyObject instance."""
	def __init__(self, py_method, instance):
		super().__init__()
		self.py_method = py_method # The actual Python method
		self.instance = instance   # The PyObject instance it is bound to
		self.name = py_method.__name__

	def execute(self, args):
		"""Handles the method calls."""
		res = RTResult()
		
		# Unwrap arguments
		unwrapped_args = [arg.py_object if isinstance(arg, PyObject) else arg.value 
						  for arg in args if hasattr(arg, 'value') or isinstance(arg, PyObject)]
		
		try:
			# Call the underlying Python method
			py_result = self.py_method(*unwrapped_args)
		except Exception as e:
			return res.failure(RTError(self.pos_start, self.pos_end, f"Python Error: {str(e)}", self.context))

		# Re-wrap the result using the PyObject's wrapper logic
		return res.success(self.instance.wrap_py_value(py_result).set_context(self.context).set_pos(self.pos_start, self.pos_end))

	def copy(self):
		copy = PyMethod(self.py_method, self.instance)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		return f'<PyMethod {self.name}>'

class BoundMethod(BaseFunction):
	def __init__(self, name, instance, method_function):
		super().__init__(name)
		self.instance = instance
		self.method_function = method_function
		self.arg_names = self.method_function.arg_names

	def execute(self, args_from_caller):
		all_args_for_method = [self.instance] + args_from_caller
		
		return self.method_function.execute(all_args_for_method)

	def copy(self):
		new_bound_method = BoundMethod(self.name, self.instance, self.method_function.copy())
		new_bound_method.set_pos(self.pos_start, self.pos_end).set_context(self.context)
		return new_bound_method

	def __repr__(self):
		return f"<Bound Method {self.instance.klass.name}.{self.name}>"

class NytescriptInstance(Value):
	def __init__(self, klass):
		super().__init__()
		self.klass = klass
		self.members = SymbolTable()

	def get_member(self, name_tok):
		member_name = name_tok.value
		value = self.members.get(member_name)
		if value:
			return value.copy().set_pos(name_tok.pos_start, name_tok.pos_end).set_context(self.context), None

		method = self.klass.methods.get(member_name)
		if method:
			bound_method = BoundMethod(member_name, self, method)
			bound_method.set_context(self.context).set_pos(name_tok.pos_start, name_tok.pos_end)
			return bound_method, None
		
		return None, RTError(
			name_tok.pos_start, name_tok.pos_end,
			f"Attribute or method '{member_name}' not found on instance of '{self.klass.name}'",
			self.context
		)

	def set_member(self, name_tok, value_to_set):
		member_name = name_tok.value
		self.members.define(member_name, value_to_set)
		return None

	def copy(self):
		new_instance = NytescriptInstance(self.klass)
		new_instance.set_pos(self.pos_start, self.pos_end).set_context(self.context)
			
		if self.members and self.members.symbols:
			for name, value in self.members.symbols.items():
				if hasattr(value, 'copy') and callable(value.copy):
					new_instance.members.define(name, value.copy())
				else:
					new_instance.members.define(name, value)

		return new_instance


	def __repr__(self):
		return f"<Instance of {self.klass.name} at 0x{id(self):x}>"

	def __str__(self):
		str_method_tok = Token(TT_IDENTIFIER, "__str__", self.pos_start, self.pos_end)
		str_method_val, _ = self.get_member(str_method_tok)
		if str_method_val and isinstance(str_method_val, BoundMethod):
			res = RTResult()
			method_call_rt_result = str_method_val.execute([]) 
			if not method_call_rt_result.error:
				str_val = method_call_rt_result.value
				if isinstance(str_val, String):
					return str_val.value
				elif isinstance(str_val, NoneType):
					pass
				else:
					return str(str_val)
		return self.__repr__() 

class NytescriptClass(BaseFunction):
	def __init__(self, name, methods, constructor_name="__init__"):
		super().__init__(name)
		self.methods = methods
		self.constructor = self.methods.get(constructor_name, None)

	def execute(self, args):
		res = RTResult()
		instance = NytescriptInstance(self)
		instance.set_context(self.context).set_pos(self.pos_start, self.pos_end)

		if self.constructor:
			constructor_rt_result = self.constructor.execute([instance] + args)
			
			if constructor_rt_result.error:
				return constructor_rt_result
		
		return res.success(instance)

	def copy(self):
		copied_methods = {name: meth.copy() for name, meth in self.methods.items()}
		new_class = NytescriptClass(self.name, copied_methods)
		new_class.constructor = copied_methods.get("__init__", None)
		new_class.set_pos(self.pos_start, self.pos_end).set_context(self.context)
		return new_class

	def __repr__(self):
		return f"<Class {self.name}>"

class ModuleValue(Value):
	def __init__(self, name, symbol_table):
		super().__init__()
		self.in_stdlib = False
		self.name = name
		if self.name in STDLIB: self.in_stdlib = True
		self.symbol_table = symbol_table

	def get_member(self, name_tok):
		if hasattr(name_tok, 'value') and hasattr(name_tok, 'pos_start'):
			member_name = name_tok.value
			pos_start = name_tok.pos_start
			pos_end = name_tok.pos_end
		else:
			member_name = str(name_tok)
			pos_start = self.pos_start # Use the object's position as a default
			pos_end = self.pos_end
		
		if not isinstance(member_name, str) or not member_name:
			return None, self.illegal_operation()

		# 2. Look up the value using the extracted string name
		value = self.symbol_table.get(member_name)

		if value is None:
			return None, RTError(
				name_tok.pos_start, name_tok.pos_end,
				f"Member '{name_tok.value}' not found in module '{self.name}'",
				self.context, "AttributeError"
			)
		copied_value = value.copy().set_pos(name_tok.pos_start, name_tok.pos_end)
		return copied_value, None

	def set_member(self, name_tok, value_to_set):
		member_name = name_tok.value
		self.symbol_table.assign(member_name, value_to_set)
		return None

	def copy(self):
		copy = ModuleValue(self.name, self.symbol_table)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return f"<{'Stdlib' if self.in_stdlib else 'Module'} {self.name}>"

	def __repr__(self):
		return f"<{'Stdlib' if self.in_stdlib else 'Module'} {self.name}>"



#######################################
# CONTEXT
#######################################

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)
		if value is None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		if name in self.symbols:
			del self.symbols[name]
		elif self.parent:
			self.parent.remove(name)
	
	def define(self, name, value):
		self.symbols[name] = value
	
	def assign(self, name, value):
		if name in self.symbols:
			self.symbols[name] = value
			return True
		if self.parent:
			return self.parent.assign(name, value)
		return False

#######################################
# INTERPRETER
#######################################

class Interpreter:
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} method defined')

	###################################

	def visit_NumberNode(self, node, context):
		return RTResult().success(
			Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_StringNode(self, node, context):
		return RTResult().success(
			String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_TemplateStringNode(self, node, context):
		res = RTResult()
		interpolated_string = ""

		for segment_node in node.segments:
			segment_value = res.register(self.visit(segment_node, context))
			if res.should_return():
				return res

			try:
				interpolated_string += str(segment_value)
			except Exception as e:
				return res.failure(RTError(
					segment_node.pos_start, segment_node.pos_end,
					f"Failed to convert value to string in f-string: {e}",
					context
				))

		return res.success(String(interpolated_string).set_context(context).set_pos(node.pos_start, node.pos_end))


	def visit_ListNode(self, node, context):
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return(): return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_VarAccessNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"'{var_name}' is not defined",
				context
			))
		
		if isinstance(value, NytescriptInstance):
			value.set_pos(node.pos_start, node.pos_end).set_context(context)
		else:
			value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
			
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RTResult()
		if node.var_name_tok.value != '_':
			var_name = node.var_name_tok.value
		else:
			return res.success(None)
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res

		if node.is_declaration:
			context.symbol_table.define(var_name, value)
		else:
			if not context.symbol_table.assign(var_name, value):
				return res.failure(RTError(
					node.var_name_tok.pos_start, node.var_name_tok.pos_end,
					f"Variable '{var_name}' is not defined. Cannot reassign.",
					context
				))
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node, context))
		if res.should_return(): return res

		if node.op_tok.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:
			result, error = left.multed_by(right)
		elif node.op_tok.type == TT_DIV:
			result, error = left.dived_by(right)
		elif node.op_tok.type == TT_POW:
			result, error = left.powed_by(right)
		elif node.op_tok.type == TT_PERCENT:
			result, error = left.percent_by(right)
		elif node.op_tok.type == TT_FDIV:
			result, error = left.fdiv_by(right)
		elif node.op_tok.type == TT_EE:
			result, error = left.get_comparison_eq(right)
		elif node.op_tok.type == TT_NE:
			result, error = left.get_comparison_ne(right)
		elif node.op_tok.type == TT_LT:
			result, error = left.get_comparison_lt(right)
		elif node.op_tok.type == TT_GT:
			result, error = left.get_comparison_gt(right)
		elif node.op_tok.type == TT_LTE:
			result, error = left.get_comparison_lte(right)
		elif node.op_tok.type == TT_GTE:
			result, error = left.get_comparison_gte(right)
		elif node.op_tok.matches(TT_KEYWORD, KEYWORDS[1]):
			result, error = left.anded_by(right)
		elif node.op_tok.matches(TT_KEYWORD, KEYWORDS[2]):
			result, error = left.ored_by(right)

		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.pos_start, node.pos_end).set_context(context))

	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		number = res.register(self.visit(node.node, context))
		if res.should_return(): return res

		error = None

		if node.op_tok.type == TT_MINUS:
			number, error = number.multed_by(Number(-1))
		elif node.op_tok.matches(TT_KEYWORD, KEYWORDS[3]):
			number, error = number.notted()

		if error:
			return res.failure(error)
		else:
			return res.success(number.set_pos(node.pos_start, node.pos_end).set_context(context))

	def visit_IfNode(self, node, context):
		res = RTResult()

		for condition, expr, should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(Number.null if should_return_null else expr_value)

		if node.else_case:
			expr, should_return_null = node.else_case
			expr_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(Number.null if should_return_null else expr_value)

		return res.success(Number.null)

	def visit_ForNode(self, node, context):
		res = RTResult()
		elements = []

		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res

		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = Number(1)

		if not isinstance(start_value, Number) or not isinstance(end_value, Number) or not isinstance(step_value, Number):
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				"For loop start, end, and step values must be numbers",
				context
			))

		if step_value.value == 0:
			return res.failure(RTError(
				step_value.pos_start, step_value.pos_end,
				"For loop step cannot be zero",
				context
			))

		i = start_value.value

		if step_value.value >= 0:
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value

		while condition():
			context.symbol_table.set(node.var_name_tok.value, Number(i).set_context(context))
			i += step_value.value

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue:
				res.loop_should_continue = False
				continue

			if res.loop_should_break:
				res.loop_should_break = False
				break

			if not node.should_return_null:
				elements.append(value)

		return res.success(
			Number.null if node.should_return_null else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_WhileNode(self, node, context):
		res = RTResult()
		elements = []

		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true():
				break

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue:
				res.loop_should_continue = False
				continue

			if res.loop_should_break:
				res.loop_should_break = False
				break

			if not node.should_return_null:
				elements.append(value)

		return res.success(
			Number.null if node.should_return_null else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_FuncDefNode(self, node, context):
		res = RTResult()

		func_name = node.var_name_tok.value if node.var_name_tok else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_toks]
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
		if node.var_name_tok:
			context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RTResult()
		args = []

		try:
			original_callable_node = node.node_to_call 
			value_to_call = res.register(self.visit(original_callable_node, context))
			if res.should_return(): return res
			
			was_class_call = isinstance(value_to_call, NytescriptClass)


			for arg_node in node.arg_nodes:
				args.append(res.register(self.visit(arg_node, context)))
				if res.should_return(): return res

			return_rt_result = value_to_call.execute(args) 
	
			if not isinstance(return_rt_result, RTResult):
				problematic_value = return_rt_result
				if isinstance(problematic_value, Value):
					problematic_value.set_pos(node.pos_start, node.pos_end).set_context(context)
				return res.success(problematic_value)

			final_value_from_call = res.register(return_rt_result)
			if res.should_return(): 
				return res 
			
			if isinstance(final_value_from_call, Value):
				if was_class_call:
					final_value_from_call.set_pos(node.pos_start, node.pos_end).set_context(context)
				else:
					final_value_from_call = final_value_from_call.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
			
			return res.success(final_value_from_call)
		except RecursionError:
			return res.failure(RecursiveError(
				node.node_to_call.pos_start, node.node_to_call.pos_end,
					f"Exceeded Call Stack Size = {sys.getrecursionlimit()}",
					context
			))

	def visit_ReturnNode(self, node, context):
		res = RTResult()

		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else:
			value = Number.null

		return res.success_return(value)

	def visit_ContinueNode(self, node, context):
		return RTResult().success_continue()

	def visit_BreakNode(self, node, context):
		return RTResult().success_break()

	def visit_PassNode(self, node, context):
		return RTResult().success(NoneType.none)

	def visit_SwitchNode(self, node, context):
		res = RTResult()
		switch_value = res.register(self.visit(node.expression_node, context))
		if res.should_return(): return res

		executed_case = False

		for condition_node, body_node in node.cases:
			case_value = res.register(self.visit(condition_node, context))
			if res.should_return(): return res

			comparison_result, error = switch_value.get_comparison_eq(case_value)
			if error: return res.failure(error)

			if comparison_result.is_true():
				body_result = res.register(self.visit(body_node, context))
				if res.should_return():
					if res.loop_should_break:
						res.loop_should_break = False
						return res.success(body_result)
					return res

				executed_case = True
				return res.success(body_result)

		if not executed_case and node.default_case:
			default_body_node = node.default_case
			default_result = res.register(self.visit(default_body_node, context))
			if res.should_return():
				if res.loop_should_break:
					res.loop_should_break = False
					return res.success(default_result)
				return res
			return res.success(default_result)


		return res.success(Number.null)

	def visit_TryExceptNode(self, node, context):
		res = RTResult()

		try_result = self.visit(node.try_body_node, context)

		if try_result.error:
			except_result = self.visit(node.except_body_node, context)
			if except_result.should_return(): return except_result
			return res.success(except_result.value)

		return res.success(try_result.value)

	def visit_ImportNode(self, node, context):
		res = RTResult()
		module_name = node.module_name_tok.value

		if module_name in STDLIB:
			lib_type, lib_content = STDLIB[module_name]
			module_scope = {}
			try:
				if lib_type == 'module':
					py_module = importlib.import_module(lib_content)
					module_scope = py_module.__dict__

				elif lib_type == 'code':
					exec(lib_content, module_scope)

			except Exception as e:
				return res.failure(RTError(
					node.pos_start, node.pos_end,
					f"Failed to load Python module '{module_name}': {e}",
					context, error_title="ImportError"
				))
			
			module_symbol_table = SymbolTable(global_symbol_table)
			
			for name, item in module_scope.items():
				if name.startswith("__"):
					continue
				if isclass(item):
					module_symbol_table.set(name, PyClass(item))
				elif callable(item):
					module_symbol_table.set(name, BuiltInMethod(name, item))
				elif isinstance(item, (int, float)):
					module_symbol_table.set(name, Number(item))
				elif isinstance(item, str):
					module_symbol_table.set(name, String(item))
					
			module_value = ModuleValue(module_name, module_symbol_table).set_context(context).set_pos(node.pos_start, node.pos_end)
			context.symbol_table.set(module_name, module_value)
			return res.success(module_value)

		filename = f"{module_name}{FILE_EXTENSION}"

		current_ctx = context
		while current_ctx:
			if current_ctx.symbol_table and current_ctx.symbol_table.get(module_name) is not None:
				return res.success(current_ctx.symbol_table.get(module_name))
			current_ctx = current_ctx.parent

		try:
			with open(filename, "r") as f:
				script = f.read()
		except FileNotFoundError:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Module '{module_name}' not found. File '{filename}' does not exist.",
				context
			))
		except Exception as e:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Failed to read module file '{filename}': {e}",
				context
			))

		module_context = Context(f"<module {module_name}>", context, node.pos_start)
		module_context.symbol_table = SymbolTable(global_symbol_table)
		_, module_error = run(filename, script, context=module_context)

		if module_error:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Error importing module '{module_name}':\n{module_error.as_string()}",
				context
			))

		module_value = ModuleValue(module_name, module_context.symbol_table).set_context(context).set_pos(node.pos_start, node.pos_end)

		context.symbol_table.set(module_name, module_value)

		return res.success(module_value)
	
	def visit_IncludeNode(self, node, context):
		res = RTResult()
		module_name = node.module_name_tok.value
		filename = f"{module_name}{FILE_EXTENSION}"

		current_ctx = context
		while current_ctx:
			if current_ctx.symbol_table and current_ctx.symbol_table.get(module_name) is not None:
				return res.success(current_ctx.symbol_table.get(module_name))
			current_ctx = current_ctx.parent
			
		if module_name in STDLIB:
			script = STDLIB[module_name]
			module_value, module_error = run(filename, script, context=None)

			if module_error:
				return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Error importing module '{module_name}':\n{module_error.as_string()}",
				context
			))

			return res.success(module_value)

		try:
			with open(filename, "r") as f:
				script = f.read()
		except FileNotFoundError:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Module '{module_name}' not found. File '{filename}' does not exist.",
				context
			))
		except Exception as e:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Failed to read module file '{filename}': {e}",
				context
			))
		module_value, module_error = run(filename, script, context=None)

		return res.success(module_value)

	def visit_MemberAccessNode(self, node, context): 
		res = RTResult()

		object_value = res.register(self.visit(node.object_node, context))
		if res.error: return res
	
		member_name = node.member_name_tok

		member_value, error = object_value.get_member(member_name)

		if error: 
			return res.failure(error)
		
		return res.success(member_value)
	
	def visit_MemberAssignNode(self, node, context):
		res = RTResult()
		
		object_value = res.register(self.visit(node.object_node, context))
		if res.should_return(): return res
		
		value_to_assign = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res

		error = object_value.set_member(node.member_name_tok, value_to_assign)
		
		if error:
			return res.failure(error)
		
		return res.success(value_to_assign)

	def visit_ClassDefNode(self, node, context):
		res = RTResult()
		class_name = node.class_name_tok.value
		
		methods = {}
		for method_node in node.method_nodes:
			method_name = method_node.var_name_tok.value if method_node.var_name_tok else None
			if not method_name:
				return res.failure(RTError(
					method_node.pos_start, method_node.pos_end,
					"Methods within a class must be named.",
					context
				))
			
			arg_names = [arg.value for arg in method_node.arg_name_toks]
			method_function = Function(
				method_name,
				method_node.body_node,
				arg_names,
				method_node.should_auto_return
			)
			method_function.set_context(context).set_pos(method_node.pos_start, method_node.pos_end)
			methods[method_name] = method_function
		
		class_value = NytescriptClass(class_name, methods)
		class_value.set_context(context).set_pos(node.pos_start, node.pos_end)
		
		context.symbol_table.define(class_name, class_value)
		
		return res.success(class_value)



#######################################
# RUN
#######################################

def symbols():
	global global_symbol_table, imported_modules
	global_symbol_table = SymbolTable()
	global_symbol_table.set(SYMBOL_TABLE[0], Number.null)
	global_symbol_table.set(SYMBOL_TABLE[1], Bool.false)
	global_symbol_table.set(SYMBOL_TABLE[2], Bool.true)
	global_symbol_table.set(SYMBOL_TABLE[3], NoneType.none)
	for i in range(4, len(SYMBOL_TABLE)):
		global_symbol_table.set(SYMBOL_TABLE[i], BuiltInFunction(SYMBOL_TABLE[i]))

	imported_modules = {}

def run(fn, text, context=None, new_context=False):

	# Generate Tokens
	lexer = Lexer(fn, text)
	tokens, error = lexer.tokeniser()
	if error: return None, error

	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run Nytescript
	interpreter = Interpreter()
	if context is None:
		context = Context('<program>')
		context.symbol_table = global_symbol_table
	elif new_context:
		context = Context('<module>', context, None)
		context.symbol_table = SymbolTable(context.parent.symbol_table)

	try:
		result = interpreter.visit(ast.node, context)
		return result.value, result.error
	except KeyboardInterrupt:
		return NoneType.none, KeyboardInterrupted(Position(0, 0, 0, fn, text), Position(0, 0, 0, fn, text))

if __name__ == __name__:
	symbols()
	run('<setup>', '')