'''
Nytescript Shell and Intepreter, written by @_nnn_ (A.K.A @FlyBoyAce2) in Python 3.12.9, 3.13.2	and 3.13.3

It is based on the interpreter https://github.com/davidcallanan/py-myopl-code by David Callanan

This is an esoteric interpreted programming Language made in Python named Nytescript. It has essential functions such as
printing, input, conditional statements, definable functions, while and for loops, and the ability to run files and
exit the programme. It supports comments in regional currency symbols £, #, € and ¥ with a format like Python for single line comments.

Nothing needs to be installed except the 'nytescript.py' file, preferably Python 3.12 and above.

© Copyright @_nnn_ 2025 - 2025
'''

#######################################
# INTERNAL IMPORTS
#######################################

import string
import os, sys, math, subprocess
import time

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
VERSION = '0.8.6'
FILE_EXTENSION = '.ns'

#######################################
# ERRORS
#######################################

class Error:
	def __init__(self, pos_start, pos_end, error_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details

	def as_string(self):
		result    = f'{self.error_name}: {self.details}\n'
		result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
		result += '\n\n' + self.string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def string_with_arrows(self, text, pos_start, pos_end):
		result = ''

		# Calculate indices
		idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
		idx_end = text.find('\n', idx_start + 1)
		if idx_end < 0: idx_end = len(text)

		# Generate each line
		line_count = pos_end.ln - pos_start.ln + 1
		for i in range(line_count):
			# Calculate line columns
			line = text[idx_start:idx_end]
			col_start = pos_start.col if i == 0 else 0
			col_end = pos_end.col if i == line_count - 1 else len(line) - 1

			# Append to result
			result += line + '\n'
			result += ' ' * col_start + '^' * (col_end - col_start)

			# Re-calculate indices
			idx_start = idx_end
			idx_end = text.find('\n', idx_start + 1)
			if idx_end < 0: idx_end = len(text)

		return result.replace('\t', '')

class IllegalCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start, pos_end, details=''):
		super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RecursiveError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Recursion Error', details)
		self.context = context

	def as_string(self):
		result    = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + self.string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'    File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Recursive Traceback (most recent call last):\n' + result

class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result    = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + self.string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'    File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result

#######################################
# STDLIB
#######################################

STDLIB = {
	"python": """
	pass
""",
	"math": """
# Constants
var pi = 3.1415926535897932384626433832795028841971693993751
var e = 2.71828182845904523536028747135266249775724709369995
var tau = 2 * pi

# Simple Functions
func add(a, b) -> a + b
func sub(a, b) -> a - b
func mul(a, b) -> a * b
func div(a, b) -> a / b
func pow(a, b) -> a ^ b
func fdiv(a, b) -> a // b
func mod(a, b) -> a % b
func sqrt(n) -> n ^ (1/2)
func cbrt(n) -> n ^ (1/3)
func exp(n) -> e ^ x
func floor(n) -> Number(n // 1)
func ceil(n) -> if n % 1 == 0 then n else Number(n // 1) + 1
func abs(n) -> if n > 0 then n else 0 - n

# Complex Functions
func gamma(n)
	var torun = `math.gamma(${Number(n)})`
	import python
	return Number(Number(torun))
end 

func log2(n)
	var torun = `math.log2(${Number(n)})`
	import python
	return Number(Number(torun))
end 

func log10(n)
	var torun = `math.log10(${Number(n)})`
	import python
	return Number(Number(torun))
end 

func log(n, b)
	var torun = `math.log10(${Number(n)})`
	import python
	var n = Number(Number(torun))

	var torun = `math.log10(${Number(b)})`
	import python
	var b = Number(Number(torun))

	return Number(n / b)
end

func factorial(n)
	var result = 1
	if n == 0 then
		return 1
	end

	for i = 0 to n then
		var result = result * (i + 1)
	end
	
	return result
end

func comb(n, k)
	if n == 0 then
		return 0
	end
	if k == 0 then
		return 0
	end

	var fn = 1
	var fk = 1
	var fnk = 1
	for i = 0 to n then 
		var fn = fn * (i + 1)
	end
	for i = 0 to k then 
		var fk = fk * (i + 1)
	end
	for i = 0 to n - k then 
		var fnk = fnk * (i + 1)
	end

    return Number(fn / (fk * fnk))
end

func fib(n)
	if n < 0 then
		return None
	elif n // 1 != n then
		return None
	elif n <= 1 then
		return n
	else
		var a = 0
		var b = 1

		for i = 2 to n + 1 then
			var temp = a
			var a = b
			var b = temp + b
		end

		return b
	end
end 
""",
	"random": """
func rand()
	var torun = 'random.random()'
	import python
	return Number(torun)
end

func randint(a, b)
	var torun = `random.randint(${a}, ${b})`
	import python
	return Number(torun)
end

func uniform(a, b)
	var torun = `random.uniform(${a}, ${b})`
	import python
	return Number(torun)
end

func randrange(start, stop, ste)
	var torun = `random.randrange(${start}, ${stop}, ${ste})`
	import python
	return Number(torun)
end
"""
}

#######################################
# POSITION
#######################################

class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def advance(self, current_char=None):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

TT_INT          = 'INT'
TT_FLOAT        = 'FLOAT'
TT_STRING       = 'STRING'
TT_FSTRING      = 'FSTRING'
TT_IDENTIFIER   = 'IDENTIFIER'
TT_KEYWORD      = 'KEYWORD'
TT_PLUS        	= 'PLUS'
TT_MINUS       	= 'MINUS'
TT_MUL         	= 'MUL'
TT_DIV         	= 'DIV'
TT_POW          = 'POW'
TT_FDIV         = 'FDIV'
TT_PERCENT      = 'PERCENT'
TT_EQ           = 'EQ'
TT_LPAREN     	= 'LPAREN'
TT_RPAREN     	= 'RPAREN'
TT_LSQUARE      = 'LSQUARE'
TT_RSQUARE      = 'RSQUARE'
TT_RBRACE       = 'RBRACE'
TT_LBRACE       = 'LBRACE'
TT_EE           = 'EE'
TT_NE           = 'NE'
TT_LT           = 'LT'
TT_GT           = 'GT'
TT_LTE          = 'LTE'
TT_GTE          = 'GTE'
TT_COMMA        = 'COMMA'
TT_ARROW        = 'ARROW'
TT_NEWLINE      = 'NEWLINE'
TT_EOF          = 'EOF'
TT_DOT          = 'DOT'

KEYWORDS = [
	'var',      # 0 Variable Declaration Statement
	'and',      # 1 AND && Operator
	'or',       # 2 OR || Operator
	'not',      # 3 NOT !! Operator
	'if',       # 4 If Conditional Statement
	'elif',     # 5 Else If Conditional Statement
	'else',     # 6 Else Conditional Statement
	'for',      # 7 For Loop Statement
	'to',       # 8 To Progression Statement
	'step',     # 9 Step Statement
	'while',    # 10 While Loop Statement
	'func',     # 11 Function Defition
	'then',     # 12 Then Statement
	'end',      # 13 Multiline Statement End
	'return',   # 14 Function Return Statement
	'continue', # 15 Continue Statement
	'break',    # 16 Loop Break Statement
	'in',       # 17 In Statement
	'switch',   # 18 Switch Statement
	'case',     # 19 Case Clause
	'default',  # 20 Default Clause
	'try',      # 21 Try Clause
	'except',   # 22 Except Clause
	'import',   # 23 Import Statement
	'pass',     # 24 Pass Statement (No-Op)
]

SYMBOL_TABLE = [
	'Null',     # 0 Null Value or (0)
	'False',    # 1 False Value or (0)
	'True',     # 2 True Value or (1)
	'None',     # 3 None Value or (NoneType)
]

class Token:
	def __init__(self, type_, value=None, pos_start=None, pos_end=None):
		self.type = type_
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = pos_end.copy()

	def matches(self, type_, value):
		return self.type == type_ and self.value == value

	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def tokeniser(self):
		tokens = []

		while self.current_char != None:

			match self.current_char:
				case self.current_char if self.current_char in ' \t':
					self.advance()
				case self.current_char if self.current_char in '#£¥€':
					self.skip_comment()
				case self.current_char if self.current_char in ';\n':
					tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
					self.advance()
				case self.current_char if self.current_char in DIGITS:
					tokens.append(self.make_number())
				case self.current_char if self.current_char in LETTERS:
					tokens.append(self.make_identifier())
				case '\"':
					tokens.append(self.make_string('\"'))
				case '\'':
					tokens.append(self.make_string('\''))
				case '`':
					token, error = self.make_fstring()
					if error: return [], error
					tokens.append(token)
				case '+':
					tokens.append(Token(TT_PLUS, pos_start=self.pos))
					self.advance()
				case '-':
					tokens.append(self.make_minus_or_arrow())
				case '*':
					tokens.append(Token(TT_MUL, pos_start=self.pos))
					self.advance()
				case '/':
					tokens.append(self.make_div_or_fdiv())
				case '^':
					tokens.append(Token(TT_POW, pos_start=self.pos))
					self.advance()
				case '%':
					tokens.append(Token(TT_PERCENT, pos_start=self.pos))
					self.advance()
				case '(':
					tokens.append(Token(TT_LPAREN, pos_start=self.pos))
					self.advance()
				case ')':
					tokens.append(Token(TT_RPAREN, pos_start=self.pos))
					self.advance()
				case '[':
					tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
					self.advance()
				case ']':
					tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
					self.advance()
				case '{':
					tokens.append(Token(TT_LBRACE, pos_start=self.pos))
					self.advance()
				case '}':
					tokens.append(Token(TT_RBRACE, pos_start=self.pos))
					self.advance()
				case '!':
					token, error = self.make_not_equals()
					if error: return [], error
					tokens.append(token)
				case '=':
					tokens.append(self.make_equals())
				case '<':
					tokens.append(self.make_less_than())
				case '>':
					tokens.append(self.make_greater_than())
				case ',':
					tokens.append(Token(TT_COMMA, pos_start=self.pos))
					self.advance()
				case '.':
					tokens.append(Token(TT_DOT, pos_start=self.pos))
					self.advance()
				case _:
					pos_start = self.pos.copy()
					char = self.current_char
					self.advance()
					return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		tokens.append(Token(TT_EOF, pos_start=self.pos))
		return tokens, None

	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
			num_str += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

	def make_string(self, string_char):
		string = ''
		pos_start = self.pos.copy()
		escape_character = False
		self.advance()

		escape_characters = {
			'n': '\n',
			't': '\t',
			'r': '\r',
			'"': '"',
			'\'': '\''
		}

		while self.current_char != None and (self.current_char != string_char or escape_character):
			if escape_character:
				string += escape_characters.get(self.current_char, self.current_char)
			else:
				if self.current_char == '\\':
					escape_character = True
					self.advance()
					continue
				else:
					string += self.current_char
			self.advance()
			escape_character = False

		self.advance()
		return Token(TT_STRING, string, pos_start, self.pos)

	def make_fstring(self):
		pos_start = self.pos.copy()
		self.advance()
		segments = []
		current_segment = ""
		in_expression = False
		brace_level = 0
		expr_start_idx = -1

		while self.current_char != None and self.current_char != '`':
			if not in_expression and self.current_char == '$' and self.peek(1) == '{':
				if current_segment:
					segments.append(('string', current_segment))
					current_segment = ""
				self.advance()
				self.advance()
				in_expression = True
				brace_level = 1
				expr_start_idx = self.pos.idx
				continue

			if in_expression:
				if self.current_char == '{':
					brace_level += 1
				elif self.current_char == '}':
					brace_level -= 1

				if self.current_char == '}' and brace_level == 0:
					if expr_start_idx == -1:
						return None, InvalidSyntaxError(self.pos, self.pos, "Unexpected '}' in f-string expression")

					expr_content = self.text[expr_start_idx : self.pos.idx]
					segments.append(('expr_content', expr_content))
					current_segment = ""
					in_expression = False
					expr_start_idx = -1
					self.advance()
					continue

				if self.current_char != None:
					self.advance()
				else:
					return None, ExpectedCharError(self.pos_start, self.pos, "Expected '}' to close f-string expression")

			else:
				if self.current_char == '\\' and self.peek(1) in ['`', '$', '\\']:
					self.advance()
					if self.current_char != None:
						current_segment += self.current_char
						self.advance()
					else:
						return None, IllegalCharError(self.pos.copy().advance(-1), self.pos, "Escape sequence not completed in f-string")
					continue

				if self.current_char != None:
					current_segment += self.current_char
					self.advance()
				else:
					break

		if self.current_char != '`':
			return None, ExpectedCharError(self.pos_start, self.pos, "Expected '`' to close f-string")

		if current_segment:
			segments.append(('string', current_segment))

		self.advance()

		return Token(TT_FSTRING, segments, pos_start, self.pos), None

	def peek(self, offset=1):
		peek_idx = self.pos.idx + offset
		if peek_idx < len(self.text):
			return self.text[peek_idx]
		return None


	def make_identifier(self):
		id_str = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()

		tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
		return Token(tok_type, id_str, pos_start, self.pos)

	def make_minus_or_arrow(self):
		tok_type = TT_MINUS
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '>':
			self.advance()
			tok_type = TT_ARROW

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_div_or_fdiv(self):
		tok_type = TT_DIV
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '/':
			self.advance()
			tok_type = TT_FDIV

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_not_equals(self):
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

		self.advance()
		return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

	def make_equals(self):
		tok_type = TT_EQ
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_EE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_less_than(self):
		tok_type = TT_LT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_LTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_greater_than(self):
		tok_type = TT_GT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_GTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def skip_comment(self):
		self.advance()

		while self.current_char != '\n':
			self.advance()

		self.advance()

#######################################
# NODES
#######################################

class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return f'{self.tok}'

class StringNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return f'{self.tok}'

class TemplateStringNode:
	def __init__(self, segments, pos_start, pos_end):
		self.segments = segments

		self.pos_start = pos_start
		self.pos_end = pos_end

	def __repr__(self):
		return f'TemplateString({self.segments})'


class ListNode:
	def __init__(self, element_nodes, pos_start, pos_end):
		self.element_nodes = element_nodes

		self.pos_start = pos_start
		self.pos_end = pos_end

class VarAccessNode:
	def __init__(self, var_name_tok):
		self.var_name_tok = var_name_tok

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
	def __init__(self, var_name_tok, value_node):
		self.var_name_tok = var_name_tok
		self.value_node = value_node

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.value_node.pos_end

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

		self.pos_start = self.op_tok.pos_start
		self.pos_end = node.pos_end

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'

class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case

		self.pos_start = self.cases[0][0].pos_start
		self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

class ForNode:
	def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
		self.var_name_tok = var_name_tok
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.step_value_node = step_value_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.body_node.pos_end

class WhileNode:
	def __init__(self, condition_node, body_node, should_return_null):
		self.condition_node = condition_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos_start = self.condition_node.pos_start
		self.pos_end = self.body_node.pos_end

class FuncDefNode:
	def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
		self.var_name_tok = var_name_tok
		self.arg_name_toks = arg_name_toks
		self.body_node = body_node
		self.should_auto_return = should_auto_return

		if self.var_name_tok:
			self.pos_start = self.var_name_tok.pos_start
		elif len(self.arg_name_toks) > 0:
			self.pos_start = self.arg_name_toks[0].pos_start
		else:
			self.pos_start = self.body_node.pos_start

		self.pos_end = self.body_node.pos_end

class CallNode:
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes

		self.pos_start = self.node_to_call.pos_start

		if len(self.arg_nodes) > 0:
			self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
		else:
			self.pos_end = self.node_to_call.pos_end

class ReturnNode:
	def __init__(self, node_to_return, pos_start, pos_end):
		self.node_to_return = node_to_return

		self.pos_start = pos_start
		self.pos_end = pos_end

class ContinueNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end

class BreakNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end

class SwitchNode:
	def __init__(self, expression_node, cases, default_case, pos_start, pos_end):
		self.expression_node = expression_node
		self.cases = cases
		self.default_case = default_case

		self.pos_start = pos_start
		self.pos_end = pos_end

class TryExceptNode:
	def __init__(self, try_body_node, except_body_node):
		self.try_body_node = try_body_node
		self.except_body_node = except_body_node

		self.pos_start = self.try_body_node.pos_start
		self.pos_end = self.except_body_node.pos_end

class PassNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end

class ImportNode:
	def __init__(self, module_name_tok):
		self.module_name_tok = module_name_tok

		self.pos_start = self.module_name_tok.pos_start
		self.pos_end = self.module_name_tok.pos_end

class MemberAccessNode:
	def __init__(self, object_node, member_name_tok):
		self.object_node = object_node
		self.member_name_tok = member_name_tok

		self.pos_start = self.object_node.pos_start
		self.pos_end = self.member_name_tok.pos_end

#######################################
# PARSE RESULT
#######################################

class ParseResult:
	def __init__(self):
		self.reset()

	def reset(self):
		self.error = None
		self.node = None
		self.last_registered_advance_count = 0
		self.advance_count = 0
		self.to_reverse_count = 0

	def register_advancement(self):
		self.last_registered_advance_count = 1
		self.advance_count += 1

	def register(self, res):
		self.last_registered_advance_count = res.advance_count
		self.advance_count += res.advance_count
		if res.error: self.error = res.error
		return res.node

	def try_register(self, res):
		if res.error:
			self.to_reverse_count = res.advance_count
			return None
		return self.register(res)

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.last_registered_advance_count == 0:
			self.error = error
		return self

	# def should_return(self):
	# 	return self.error is not None

#######################################
# PARSER -> AST
#######################################

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.advance()

	def advance(self):
		self.tok_idx += 1
		self.update_current_tok()
		return self.current_tok

	def reverse(self, amount=1):
		self.tok_idx -= amount
		self.update_current_tok()
		return self.current_tok

	def update_current_tok(self):
		if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]

	def parse(self):
		res = self.statements()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Token cannot appear after previous tokens"
			))
		return res

	###################################

	def statements(self):
		res = ParseResult()
		statements = []
		pos_start = self.current_tok.pos_start.copy()

		while self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

		statement = res.register(self.statement())
		if res.error: return res
		statements.append(statement)

		more_statements = True

		while True:
			newline_count = 0
			while self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()
				newline_count += 1
			if newline_count == 0:
				more_statements = False

			if not more_statements: break
			statement = res.try_register(self.statement())
			if not statement:
				self.reverse(res.to_reverse_count)
				more_statements = False
				continue
			statements.append(statement)

		return res.success(ListNode(
			statements,
			pos_start,
			self.current_tok.pos_end.copy()
		))

	def statement(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[14]):
			res.register_advancement()
			self.advance()

			expr = res.try_register(self.expr())
			if not expr:
				self.reverse(res.to_reverse_count)
			return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[15]):
			res.register_advancement()
			self.advance()
			return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[16]):
			res.register_advancement()
			self.advance()
			return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[24]):
			res.register_advancement()
			self.advance()
			return res.success(PassNode(pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[21]):
			try_except_node = res.register(self.try_except_expr())
			if res.error: return res
			return res.success(try_except_node)

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[23]):
			import_node = res.register(self.import_expr())
			if res.error: return res
			return res.success(import_node)


		expr = res.register(self.expr())
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[14]}', '{KEYWORDS[15]}', '{KEYWORDS[16]}', '{KEYWORDS[0]}', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}', '{KEYWORDS[23]}', '{KEYWORDS[24]}', int, float, identifier, '+', '-', '(', '[' or '{KEYWORDS[3]}'"
			))
		return res.success(expr)

	def import_expr(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[23]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[23]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_IDENTIFIER:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected identifier after '{KEYWORDS[23]}'"
			))

		module_name_tok = self.current_tok
		res.register_advancement()
		self.advance()

		return res.success(ImportNode(module_name_tok))


	def expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[0]):
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier"
				))

			var_name = self.current_tok
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_EQ:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '='"
				))

			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res
			return res.success(VarAssignNode(var_name, expr))

		node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, KEYWORDS[1]), (TT_KEYWORD, KEYWORDS[2]))))

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[0]}', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}', '{KEYWORDS[23]}', int, float, identifier, '+', '-', '(', '[' or '{KEYWORDS[3]}'"
			))

		return res.success(node)

	def comp_expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[3]):
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()

			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(UnaryOpNode(op_tok, node))

		node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected int, float, identifier, '+', '-', '(', '[', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}', '{KEYWORDS[23]}' or '{KEYWORDS[3]}'"
			))

		return res.success(node)

	def arith_expr(self):
		return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_FDIV, TT_PERCENT))

	def factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			res.register_advancement()
			self.advance()
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))

		return self.power()

	def power(self):
		return self.bin_op(self.call, (TT_POW, ), self.factor)

	def call(self):
		res = ParseResult()
		atom = res.register(self.member_access())
		if res.error: return res

		if self.current_tok.type == TT_LPAREN:
			res.register_advancement()
			self.advance()
			arg_nodes = []

			if self.current_tok.type == TT_RPAREN:
				res.register_advancement()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expr()))
				if res.error:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected ')', '{KEYWORDS[0]}', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}', '{KEYWORDS[23]}', int, float, identifier, '+', '-', '(', '[' or '{KEYWORDS[3]}'"
					))

				while self.current_tok.type == TT_COMMA:
					res.register_advancement()
					self.advance()

					arg_nodes.append(res.register(self.expr()))
					if res.error: return res

				if self.current_tok.type != TT_RPAREN:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected ',' or ')'"
					))

				res.register_advancement()
				self.advance()
			return res.success(CallNode(atom, arg_nodes))
		return res.success(atom)

	def member_access(self):
		res = ParseResult()
		node = res.register(self.atom())
		if res.error: return res

		while self.current_tok.type == TT_DOT:
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier after '.'"
				))

			member_name_tok = self.current_tok
			res.register_advancement()
			self.advance()

			node = MemberAccessNode(node, member_name_tok)

		return res.success(node)


	def atom(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT):
			res.register_advancement()
			self.advance()
			return res.success(NumberNode(tok))

		elif tok.type == TT_STRING:
			res.register_advancement()
			self.advance()
			return res.success(StringNode(tok))

		elif tok.type == TT_FSTRING:
			pos_start = tok.pos_start.copy()
			segments = []

			for segment_type, segment_content in tok.value:
				if segment_type == 'string':
					segment_pos_start = pos_start.copy().advance(self.tokens[self.tok_idx].pos_start.idx - pos_start.idx)
					segment_pos_end = segment_pos_start.copy().advance(len(segment_content))
					segments.append(StringNode(Token(TT_STRING, segment_content, segment_pos_start, segment_pos_end)))
				elif segment_type == 'expr_content':
					expr_pos_start = pos_start.copy().advance(self.tokens[self.tok_idx].pos_start.idx - pos_start.idx + segment_content.find(segment_content))
					expr_lexer = Lexer(self.tokens[0].pos_start.fn, segment_content)
					expr_tokens, error = expr_lexer.tokeniser()
					if error:
						if error.pos_start:
							error.pos_start.idx += expr_pos_start.idx
							error.pos_start.col += expr_pos_start.col
						if error.pos_end:
							error.pos_end.idx += expr_pos_start.idx
							error.pos_end.col += expr_pos_start.col
						return res.failure(error)

					expr_parser = Parser(expr_tokens)
					expr_node = res.register(expr_parser.expr())
					if res.error:
						if res.error.pos_start:
							res.error.pos_start.idx += expr_pos_start.idx
							res.error.pos_start.col += expr_pos_start.col
						if res.error.pos_end:
							res.error.pos_end.idx += expr_pos_start.idx
							res.error.pos_end.col += expr_pos_start.col
						res.error.details = f"Error in f-string expression: {res.error.details}"
						return res

					segments.append(expr_node)

			res.register_advancement()
			self.advance()

			return res.success(TemplateStringNode(segments, pos_start, tok.pos_end))


		elif tok.type == TT_IDENTIFIER:
			res.register_advancement()
			self.advance()
			return res.success(VarAccessNode(tok))

		elif tok.type == TT_LPAREN:
			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register_advancement()
				self.advance()
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))

		elif tok.type == TT_LSQUARE:
			list_expr = res.register(self.list_expr())
			if res.error: return res
			return res.success(list_expr)

		elif tok.matches(TT_KEYWORD, KEYWORDS[4]):
			if_expr = res.register(self.if_expr())
			if res.error: return res
			return res.success(if_expr)

		elif tok.matches(TT_KEYWORD, KEYWORDS[7]):
			for_expr = res.register(self.for_expr())
			if res.error: return res
			return res.success(for_expr)

		elif tok.matches(TT_KEYWORD, KEYWORDS[10]):
			while_expr = res.register(self.while_expr())
			if res.error: return res
			return res.success(while_expr)

		elif tok.matches(TT_KEYWORD, KEYWORDS[11]):
			func_def = res.register(self.func_def())
			if res.error: return res
			return res.success(func_def)

		elif tok.matches(TT_KEYWORD, KEYWORDS[18]):
			switch_expr = res.register(self.switch_expr())
			if res.error: return res
			return res.success(switch_expr)

		elif tok.matches(TT_KEYWORD, KEYWORDS[21]):
			try_except_node = res.register(self.try_except_expr())
			if res.error: return res
			return res.success(try_except_node)

		return res.failure(InvalidSyntaxError(
			tok.pos_start, tok.pos_end,
			f"Expected int, float, identifier, '+', '-', '(', '[', '{KEYWORDS[0]}', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}'"
		))

	def list_expr(self):
		res = ParseResult()
		element_nodes = []
		pos_start = self.current_tok.pos_start.copy()

		if self.current_tok.type != TT_LSQUARE:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '['"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_RSQUARE:
			res.register_advancement()
			self.advance()
		else:
			element_nodes.append(res.register(self.expr()))
			if res.error:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected ']', '{KEYWORDS[0]}', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}', '{KEYWORDS[23]}', int, float, identifier, '+', '-', '(', '[' or '{KEYWORDS[3]}'"
				))

			while self.current_tok.type == TT_COMMA:
				res.register_advancement()
				self.advance()

				element_nodes.append(res.register(self.expr()))
				if res.error: return res

			if self.current_tok.type != TT_RSQUARE:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected ',' or ']'"
				))

			res.register_advancement()
			self.advance()

		return res.success(ListNode(
			element_nodes,
			pos_start,
			self.current_tok.pos_end.copy()
		))

	def if_expr(self):
		res = ParseResult()
		all_cases = res.register(self.if_expr_cases(KEYWORDS[4]))
		if res.error: return res
		cases, else_case = all_cases
		return res.success(IfNode(cases, else_case))

	def if_expr_b(self):
		return self.if_expr_cases(KEYWORDS[5])

	def if_expr_c(self):
		res = ParseResult()
		else_case = None

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[6]):
			res.register_advancement()
			self.advance()

			if self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()

				statements = res.register(self.statements())
				if res.error: return res
				else_case = (statements, True)

				if self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
					res.register_advancement()
					self.advance()
				else:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected {KEYWORDS[13]}"
					))
			else:
				expr = res.register(self.statement())
				if res.error: return res
				else_case = (expr, False)

		return res.success(else_case)

	def if_expr_b_or_c(self):
		res = ParseResult()
		cases, else_case = [], None

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[5]):
			all_cases = res.register(self.if_expr_b())
			if res.error: return res
			new_cases, else_case = all_cases
			cases.extend(new_cases)
		else:
			else_case = res.register(self.if_expr_c())
			if res.error: return res

		return res.success((cases, else_case))

	def if_expr_cases(self, case_keyword):
		res = ParseResult()
		cases = []
		else_case = None

		if not self.current_tok.matches(TT_KEYWORD, case_keyword):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{case_keyword}'"
			))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if res.error: return res

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[12]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[12]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

			statements = res.register(self.statements())
			if res.error: return res
			cases.append((condition, statements, True))

			if self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
				res.register_advancement()
				self.advance()
			else:
				all_cases = res.register(self.if_expr_b_or_c())
				if res.error: return res
				new_cases, else_case = all_cases
				cases.extend(new_cases)
		else:
			expr = res.register(self.statement())
			if res.error: return res
			cases.append((condition, expr, False))

			all_cases = res.register(self.if_expr_b_or_c())
			if res.error: return res
			new_cases, else_case = all_cases
			cases.extend(new_cases)

		return res.success((cases, else_case))

	def for_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[7]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[7]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_IDENTIFIER:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected identifier"
			))

		var_name = self.current_tok
		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_EQ:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '='"
			))

		res.register_advancement()
		self.advance()

		start_value = res.register(self.expr())
		if res.error: return res

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[8]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[8]}'"
			))

		res.register_advancement()
		self.advance()

		end_value = res.register(self.expr())
		if res.error: return res

		if self.current_tok.matches(TT_KEYWORD, KEYWORDS[9]):
			res.register_advancement()
			self.advance()

			step_value = res.register(self.expr())
			if res.error: return res
		else:
			step_value = None

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[12]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[12]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

			body = res.register(self.statements())
			if res.error: return res

			if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '{KEYWORDS[13]}'"
				))

			res.register_advancement()
			self.advance()

			return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

		body = res.register(self.statement())
		if res.error: return res

		return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

	def while_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[10]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[10]}'"
			))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if res.error: return res

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[12]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[12]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

			body = res.register(self.statements())
			if res.error: return res

			if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '{KEYWORDS[13]}'"
				))

			res.register_advancement()
			self.advance()

			return res.success(WhileNode(condition, body, True))

		body = res.register(self.statement())
		if res.error: return res

		return res.success(WhileNode(condition, body, False))

	def func_def(self):
		res = ParseResult()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[11]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[11]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_IDENTIFIER:
			var_name_tok = self.current_tok
			res.register_advancement()
			self.advance()
			if self.current_tok.type != TT_LPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '('"
				))
		else:
			var_name_tok = None
			if self.current_tok.type != TT_LPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected identifier or '('"
				))

		res.register_advancement()
		self.advance()
		arg_name_toks = []

		if self.current_tok.type == TT_IDENTIFIER:
			arg_name_toks.append(self.current_tok)
			res.register_advancement()
			self.advance()

			while self.current_tok.type == TT_COMMA:
				res.register_advancement()
				self.advance()

				if self.current_tok.type != TT_IDENTIFIER:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected identifier"
					))

				arg_name_toks.append(self.current_tok)
				res.register_advancement()
				self.advance()

			if self.current_tok.type != TT_RPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected ',' or ')'"
				))
		else:
			if self.current_tok.type != TT_RPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected identifier or ')'"
				))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_ARROW:
			res.register_advancement()
			self.advance()

			body = res.register(self.expr())
			if res.error: return res

			return res.success(FuncDefNode(
				var_name_tok,
				arg_name_toks,
				body,
				True
			))

		if self.current_tok.type != TT_NEWLINE:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '->' or NEWLINE"
			))

		res.register_advancement()
		self.advance()

		body = res.register(self.statements())
		if res.error: return res

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[13]}'"
			))

		res.register_advancement()
		self.advance()

		return res.success(FuncDefNode(
			var_name_tok,
			arg_name_toks,
			body,
			False
		))

	def switch_expr(self):
		res = ParseResult()
		cases = []
		default_case = None
		pos_start = self.current_tok.pos_start.copy()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[18]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[18]}'"
			))

		res.register_advancement()
		self.advance()

		expression_node = res.register(self.expr())
		if res.error:
			return res

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[12]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[12]}' after {KEYWORDS[18]} expression"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_NEWLINE:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected NEWLINE after '{KEYWORDS[12]}' following {KEYWORDS[18]} expression"
			))

		res.register_advancement()
		self.advance()


		while self.current_tok.matches(TT_KEYWORD, KEYWORDS[19]) or self.current_tok.matches(TT_KEYWORD, KEYWORDS[20]):
			if self.current_tok.matches(TT_KEYWORD, KEYWORDS[19]):
				res.register_advancement()
				self.advance()

				condition_node = res.register(self.expr())
				if res.error:
					return res


				if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[12]):
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected '{KEYWORDS[12]}' after {KEYWORDS[19]} condition"
					))

				res.register_advancement()
				self.advance()

				if self.current_tok.type != TT_NEWLINE:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected NEWLINE after '{KEYWORDS[12]}' for case body"
					))

				res.register_advancement()
				self.advance()

				body_node = res.register(self.statements())
				if res.error:
					return res

				if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected '{KEYWORDS[13]}' after {KEYWORDS[19]} body"
					))
				res.register_advancement()
				self.advance()

				if self.current_tok.type != TT_NEWLINE:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected NEWLINE after '{KEYWORDS[13]}' for case body"
					))

				res.register_advancement()
				self.advance()

				cases.append((condition_node, body_node))

			elif self.current_tok.matches(TT_KEYWORD, KEYWORDS[20]):
				if default_case is not None:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Only one '{KEYWORDS[20]}' clause is allowed in a {KEYWORDS[18]} statement"
					))

				res.register_advancement()
				self.advance()


				if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[12]):
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected '{KEYWORDS[12]}' after '{KEYWORDS[20]}'"
					))

				res.register_advancement()
				self.advance()

				if self.current_tok.type != TT_NEWLINE:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected NEWLINE after '{KEYWORDS[12]}' for {KEYWORDS[20]} body"
					))

				res.register_advancement()
				self.advance()

				body_node = res.register(self.statements())
				if res.error:
					return res

				if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected '{KEYWORDS[13]}' after {KEYWORDS[20]} body"
					))
				res.register_advancement()
				self.advance()

				if self.current_tok.type != TT_NEWLINE:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected NEWLINE after '{KEYWORDS[13]}' for {KEYWORDS[19]} body"
					))

				res.register_advancement()
				self.advance()

				default_case = body_node


		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
			if self.current_tok.type == TT_EOF:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '{KEYWORDS[13]}' to close the {KEYWORDS[18]} statement, but found EOF"
				))

			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[19]}', '{KEYWORDS[20]}', or '{KEYWORDS[13]}' to close the {KEYWORDS[18]} statement"
			))

		res.register_advancement()
		self.advance()


		return res.success(SwitchNode(
			expression_node,
			cases,
			default_case,
			pos_start,
			self.current_tok.pos_end.copy()
		))

	def try_except_expr(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[21]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[21]}'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

			try_body = res.try_register(self.statements())
			if try_body:
				if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected '{KEYWORDS[13]}'"
					))
				res.register_advancement()
				self.advance()
			else:
				self.reverse(res.to_reverse_count)
				try_body = res.register(self.statement())
				if res.error: return res

			# Expect 'except' keyword
			if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[22]):
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '{KEYWORDS[22]}'"
				))
			res.register_advancement()
			self.advance()

			if self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()

				except_body = res.try_register(self.statements())
				if except_body:
					if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
						return res.failure(InvalidSyntaxError(
							self.current_tok.pos_start, self.current_tok.pos_end,
							f"Expected '{KEYWORDS[13]}'"
						))
					res.register_advancement()
					self.advance()
				else:
					self.reverse(res.to_reverse_count)
					except_body = res.register(self.statement())
					if res.error: return res

				if self.current_tok.type == TT_NEWLINE:
					res.register_advancement()
					self.advance()

				return res.success(TryExceptNode(try_body, except_body))
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected NEWLINE after '{KEYWORDS[22]}'"
				))

		else:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected NEWLINE after '{KEYWORDS[21]}'"
			))


	###################################

	def bin_op(self, func_a, ops, func_b=None):
		if func_b == None:
			func_b = func_a

		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)

#######################################
# RUNTIME RESULT
#######################################

class RTResult:
	def __init__(self):
		self.reset()

	def reset(self):
		self.value = None
		self.error = None
		self.func_return_value = None
		self.loop_should_continue = False
		self.loop_should_break = False
		self.should_exit_switch = False

	def register(self, res):
		self.error = res.error
		self.func_return_value = res.func_return_value
		self.loop_should_continue = res.loop_should_continue
		self.loop_should_break = res.loop_should_break
		self.should_exit_switch = res.should_exit_switch
		return res.value

	def success(self, value):
		self.reset()
		self.value = value
		return self

	def success_return(self, value):
		self.reset()
		self.func_return_value = value
		return self

	def success_continue(self):
		self.reset()
		self.loop_should_continue = True
		return self

	def success_break(self):
		self.reset()
		self.loop_should_break = True
		return self

	def success_exit_switch(self):
		self.reset()
		self.should_exit_switch = True
		return self


	def failure(self, error):
		self.reset()
		self.error = error
		return self

	def should_return(self):
		return (
			self.error or
			self.func_return_value or
			self.loop_should_continue or
			self.loop_should_break or
			self.should_exit_switch
		)

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
			self.context
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
					self.context
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
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def anded_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def ored_by(self, other):
		if isinstance(other, Number):
			return Number(int(self.value or other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

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
Number.false = Number(0)
Number.true = Number(1)

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
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, String):
			return Number(int(self.value != other.value)).set_context(self.context), None
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
		return f'"{self.value}"'

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
				return Number.false.set_context(self.context), None
			for i in range(len(self.elements)):
				comparison_result, error = self.elements[i].get_comparison_eq(other.elements[i])
				if error: return None, error
				if not comparison_result.is_true():
					return Number.false.set_context(self.context), None
			return Number.true.set_context(self.context), None
		else:
			return Number.false.set_context(self.context), None

	def get_comparison_ne(self, other):
		comparison_result, error = self.get_comparison_eq(other)
		if error: return None, error
		return Number(1 - comparison_result.value).set_context(self.context), None

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
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context


	def check_args(self, arg_names, args):
		res = RTResult()

		if len(args) == 0:
			return res.success(NoneType())

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

	def execute(self, args):
		res = RTResult()
		interpreter = Interpreter()
		exec_ctx = self.generate_new_context()

		res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		if res.should_return(): return res

		value = res.register(interpreter.visit(self.body_node, exec_ctx))

		if res.should_return() and res.func_return_value == None: return res

		ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
		return res.success(ret_value)

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
		sys.exit()
		return RTResult().success(NoneType.none)
	execute_exit.arg_names = []

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
				return RTResult().success(Number.true)
			return RTResult().success(Number.false)

		elif isinstance(iterable_value, List):
			for element in iterable_value.elements:
				comparison_result, error = element.get_comparison_eq(item_value)
				if error: return RTResult().failure(error)
				if comparison_result.is_true():
					return RTResult().success(Number.true)
			return RTResult().success(Number.false)

		else:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				f"First argument to is_in must be an iterable (String or List), not '{type(iterable_value).__name__}'",
				exec_ctx
			))
	execute_is_in.arg_names = ["list", "value"]

	def execute_is_number(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
		return RTResult().success(Number.true if is_number else Number.false)
	execute_is_number.arg_names = ["value"]

	def execute_is_string(self, exec_ctx):
		is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
		return RTResult().success(Number.true if is_string else Number.false)
	execute_is_string.arg_names = ["value"]

	def execute_is_list(self, exec_ctx):
		is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
		return RTResult().success(Number.true if is_list else Number.false)
	execute_is_list.arg_names = ["value"]

	def execute_is_function(self, exec_ctx):
		is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
		return RTResult().success(Number.true if is_function else Number.false)
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


BuiltInFunction.print         = BuiltInFunction("print")
BuiltInFunction.print_ret     = BuiltInFunction("print_ret")
BuiltInFunction.input         = BuiltInFunction("input")
BuiltInFunction.input_int     = BuiltInFunction("input_int")
BuiltInFunction.input_char    = BuiltInFunction("input_char")
BuiltInFunction.clear         = BuiltInFunction("clear")
BuiltInFunction.cls           = BuiltInFunction("clear")
BuiltInFunction.progress      = BuiltInFunction("progress")
BuiltInFunction.String        = BuiltInFunction("String")
BuiltInFunction.Number        = BuiltInFunction("Number")
BuiltInFunction.List          = BuiltInFunction("List")
BuiltInFunction.strcon        = BuiltInFunction("strcon")
BuiltInFunction.is_in         = BuiltInFunction("is_in")
BuiltInFunction.is_number     = BuiltInFunction("is_number")
BuiltInFunction.is_string     = BuiltInFunction("is_string")
BuiltInFunction.is_list       = BuiltInFunction("is_list")
BuiltInFunction.is_function   = BuiltInFunction("is_function")
BuiltInFunction.sorted        = BuiltInFunction("sorted")
BuiltInFunction.append        = BuiltInFunction("append")
BuiltInFunction.pop           = BuiltInFunction("pop")
BuiltInFunction.extend        = BuiltInFunction("extend")
BuiltInFunction.len		   	  = BuiltInFunction("len")
BuiltInFunction.run			  = BuiltInFunction("run")
BuiltInFunction.exit          = BuiltInFunction("exit")

class ModuleValue(Value):
	def __init__(self, name, symbol_table):
		super().__init__()
		self.in_stdlib = False
		self.name = name
		if self.name in STDLIB: self.in_stdlib = True
		self.symbol_table = symbol_table

	def get_member(self, name):
		value = self.symbol_table.get(name)
		if value is None:
			return None, RTError(
				self.pos_start, self.pos_end,
				f"Member '{name}' not found in module '{self.name}'",
				self.context
			)
		return value.copy().set_pos(self.pos_start, self.pos_end).set_context(self.context), None

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
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		if name in self.symbols:
			del self.symbols[name]
		elif self.parent:
			self.parent.remove(name)

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

		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res

		context.symbol_table.set(var_name, value)
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
			value_to_call = res.register(self.visit(node.node_to_call, context))
			if res.should_return(): return res
			value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

			if not isinstance(value_to_call, BaseFunction):
				return res.failure(RTError(
					node.node_to_call.pos_start, node.node_to_call.pos_end,
					f"Cannot call value of type '{type(value_to_call).__name__}'. Expected a function.",
					context
				))

			for arg_node in node.arg_nodes:
				args.append(res.register(self.visit(arg_node, context)))
				if res.should_return(): return res

			return_value = res.register(value_to_call.execute(args))
			if res.should_return(): return res
			return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
			return res.success(return_value)
		except RecursionError:
			return res.failure(RecursiveError(
				node.node_to_call.pos_start, node.node_to_call.pos_end,
					f"Exceeded Call Stack Size: {sys.getrecursionlimit()}",
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
		return RTResult().success(Number.null)

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
		filename = f"{module_name}{FILE_EXTENSION}"

		current_ctx = context
		while current_ctx:
			if current_ctx.symbol_table and current_ctx.symbol_table.get(module_name) is not None:
				return res.success(current_ctx.symbol_table.get(module_name))
			current_ctx = current_ctx.parent
			
		if module_name in STDLIB:
			if module_name == 'python':
				var_name = 'torun'
				value = context.symbol_table.get(var_name)

				if not value:
					return res.failure(RTError(
						node.pos_start, node.pos_end,
						f"'{var_name}' is not defined",
						context
					))

				executable = f'''import math, random, time, datetime, os, sys, re, json, platform
print({value})'''
				try:
					result = subprocess.run(
            			[sys.executable, "-c", executable],
            			capture_output=True,
            			text=True,
            			check=True
       				)
					result = result.stdout.removesuffix('\n')
				except subprocess.CalledProcessError as e:
					return res.failure(RTError(
						node.pos_start, node.pos_end,
						f"Failed to run Subprocess, {e.stderr}",
						context
					))


				context.symbol_table.set(var_name, String(result))
				return res.success(result) 
			
			else:
				script = STDLIB[module_name]
				module_context = Context(f"<STDLIB {module_name}>", context, node.pos_start)
				module_context.symbol_table = SymbolTable(global_symbol_table)
				module_result_value, module_error = run(filename, script, context=module_context)

				if module_error:
					return res.failure(RTError(
						node.pos_start, node.pos_end,
						f"Error importing module '{module_name}':\n{module_error.as_string()}",
						context
				))

				module_value = ModuleValue(module_name, module_context.symbol_table).set_context(context).set_pos(node.pos_start, node.pos_end)

				context.symbol_table.set(module_name, module_value)

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

		module_context = Context(f"<module {module_name}>", context, node.pos_start)
		module_context.symbol_table = SymbolTable(global_symbol_table)
		module_result_value, module_error = run(filename, script, context=module_context)

		if module_error:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				f"Error importing module '{module_name}':\n{module_error.as_string()}",
				context
			))

		module_value = ModuleValue(module_name, module_context.symbol_table).set_context(context).set_pos(node.pos_start, node.pos_end)

		context.symbol_table.set(module_name, module_value)

		return res.success(module_value)

	def visit_MemberAccessNode(self, node, context):
		res = RTResult()
		object_value = res.register(self.visit(node.object_node, context))
		if res.should_return(): return res

		member_name = node.member_name_tok.value

		if not hasattr(object_value, 'get_member') or not callable(object_value.get_member):
			return res.failure(RTError(
				node.object_node.pos_start, node.object_node.pos_end,
				f"'{type(object_value).__name__}' object has no attribute or member access",
				context
			))

		member_value, error = object_value.get_member(member_name)
		if error: return res.failure(error)

		return res.success(member_value.set_pos(node.pos_start, node.pos_end).set_context(context))


#######################################
# RUN
#######################################

global_symbol_table = SymbolTable()
global_symbol_table.set(SYMBOL_TABLE[0], Number.null)
global_symbol_table.set(SYMBOL_TABLE[1], Number.false)
global_symbol_table.set(SYMBOL_TABLE[2], Number.true)
global_symbol_table.set(SYMBOL_TABLE[3], NoneType.none)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("print_ret", BuiltInFunction.print_ret)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("input_char", BuiltInFunction.input_char)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("Number", BuiltInFunction.Number)
global_symbol_table.set("String", BuiltInFunction.String)
global_symbol_table.set("List", BuiltInFunction.List)
global_symbol_table.set("strcon", BuiltInFunction.strcon)
global_symbol_table.set("is_in", BuiltInFunction.is_in)
global_symbol_table.set("is_num", BuiltInFunction.is_number)
global_symbol_table.set("is_str", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_function", BuiltInFunction.is_function)
global_symbol_table.set("sorted", BuiltInFunction.sorted)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("exit", BuiltInFunction.exit)
# global_symbol_table.set("cached_func", BuiltInFunction.cached_func)

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


	result = interpreter.visit(ast.node, context)

	return result.value, result.error