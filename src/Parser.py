from Errors import InvalidSyntaxError
from Lexer import *
from Nodes import *

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
			return res.success(VarAssignNode(var_name, expr, is_declaration=True))

		node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, KEYWORDS[1]), (TT_KEYWORD, KEYWORDS[2]))))

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[0]}', '{KEYWORDS[4]}', '{KEYWORDS[7]}', '{KEYWORDS[10]}', '{KEYWORDS[11]}', '{KEYWORDS[18]}', '{KEYWORDS[21]}', '{KEYWORDS[23]}', int, float, identifier, '+', '-', '(', '[' or '{KEYWORDS[3]}'"
			))

		if self.current_tok.type == TT_EQ:
			op_tok = self.current_tok
			res.register_advancement(); self.advance()
			right_value_expr = res.register(self.expr())
			if res.error: return res

			if isinstance(node, VarAccessNode):
				return res.success(VarAssignNode(node.var_name_tok, right_value_expr, is_declaration=False))
			elif isinstance(node, MemberAccessNode):
				return res.success(MemberAssignNode(node.object_node, node.member_name_tok, right_value_expr))
			else:
				return res.failure(InvalidSyntaxError(
					node.pos_start, op_tok.pos_end,
					"Invalid assignment target. Must be an identifier or member access."
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

	def class_def(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[25]): # CLASS
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[25]}'"
			))
		res.register_advancement(); self.advance()

		if self.current_tok.type != TT_IDENTIFIER:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected class name (identifier)"
			))
		class_name_tok = self.current_tok
		res.register_advancement(); self.advance()

		if self.current_tok.type != TT_NEWLINE:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected newline after class name"
			))
		res.register_advancement(); self.advance()

		method_nodes = []
		while not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
			while self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()

			if self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
				break
			if self.current_tok.type == TT_EOF:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '{KEYWORDS[11]}' or '{KEYWORDS[13]}' for class definition, found EOF"
				))

			if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[11]):
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '{KEYWORDS[11]}' for method definition or '{KEYWORDS[13]}' to close class"
				))

			method_node = res.register(self.func_def())
			if res.error: return res
			method_nodes.append(method_node)

		if not self.current_tok.matches(TT_KEYWORD, KEYWORDS[13]):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{KEYWORDS[13]}' to close class definition"
			))

		pos_end = self.current_tok.pos_end.copy()
		res.register_advancement(); self.advance()

		return res.success(ClassDefNode(class_name_tok, method_nodes, pos_start, pos_end))

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
		
		elif tok.matches(TT_KEYWORD, KEYWORDS[25]):
			class_def_node = res.register(self.class_def())
			if res.error: return res
			return res.success(class_def_node)

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
