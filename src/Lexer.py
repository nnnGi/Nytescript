from Errors import ExpectedCharError, IllegalCharError, InvalidSyntaxError
from ConstantData import DIGITS, LETTERS, LETTERS_DIGITS
from Tokens import *

#######################################
# TOKENS & KEYWORDS
#######################################

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
	'class',    # 25 Class Declaration
	'exit',     # 26 Exit Statement
]

SYMBOL_TABLE = [
	'Null',        # 0 Null Value or (0)
	'False',       # 1 False Value or (0)
	'True',        # 2 True Value or (1)
	'None',        # 3 None Value or (NoneType)
	'print',       # 4
	'print_ret',   # 5
	'input',       # 6 
	'input_int',   # 7 
	'input_char',  # 8 
	'clear',       # 9
	'Number',      # 10
	'String',      # 11
	'List',        # 12
	'strcon',      # 13
	'is_in',       # 14
	'is_num',      # 15
	'is_str',      # 16
	'is_list',     # 17
	'is_function', # 18
	'sorted',      # 19
	'append',      # 20
	'pop',         # 21
	'extend',      # 22
	'len',         # 23
	'run',         # 24
	'exit',        # 25
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

		try:
			while self.current_char != '\n':
				self.advance()
		except KeyboardInterrupt:
			pass

		self.advance()