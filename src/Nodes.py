from Data import sys

#######################################
# NODES
#######################################

class Node:
	def to_string(self, indent=0):
		"""Base method for string representation, to be overridden by subclasses."""
		return f'{"  " * indent}{self.__class__.__name__}'

class NumberNode(Node):
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return f'{self.tok}'
	
	def to_string(self, indent=0):
		return f'{"  " * indent}NumberNode: {self.tok.value}'

class StringNode(Node):
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return f'{self.tok}'
	
	def to_string(self, indent=0):
		return f'{"  " * indent}StringNode: {self.tok.value}'

class TemplateStringNode(Node):
	def __init__(self, segments, pos_start, pos_end):
		self.segments = segments

		self.pos_start = pos_start
		self.pos_end = pos_end

	def __repr__(self):
		return f'TemplateString({self.segments})'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}TemplateStringNode:\n'
		for segment in self.segments:
			s += f'{"  " * (indent + 1)}Segment:\n'
			s += segment.to_string(indent + 2) + '\n'
		return s.rstrip()

class ListNode(Node):
	def __init__(self, element_nodes, pos_start, pos_end):
		self.element_nodes = element_nodes

		self.pos_start = pos_start
		self.pos_end = pos_end
	
	def __repr__(self):
		return f'[{','.join(self.element_nodes.__repr__())}]'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}ListNode:\n'
		for node in self.element_nodes:
			s += f'{node.to_string(indent + 1)}\n'
		return s.rstrip()

class VarAccessNode(Node):
	def __init__(self, var_name_tok):
		self.var_name_tok = var_name_tok

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.var_name_tok.pos_end
	
	def __repr__(self):
		return f'VarAccess({self.var_name_tok})'
	
	def to_string(self, indent=0):
		return f'{"  " * indent}VarAccessNode: {self.var_name_tok.value}'

class VarAssignNode(Node):
	def __init__(self, var_name_tok, value_node, is_declaration):
		self.var_name_tok = var_name_tok
		self.value_node = value_node
		self.is_declaration = is_declaration
		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.value_node.pos_end
	
	def __repr__(self):
		return f'VarAssign({self.var_name_tok}, {self.value_node})'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}VarAssignNode: {self.var_name_tok.value}\n'
		s += f'{"  " * (indent + 1)}Value:\n'
		s += self.value_node.to_string(indent + 2)
		return s

class BinOpNode(Node):
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return f'BinOp({self.left_node}, {self.op_tok}, {self.right_node})'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}BinOpNode ({self.op_tok.type}):\n'
		s += f'{"  " * (indent + 1)}Left:\n'
		s += self.left_node.to_string(indent + 2) + '\n'
		s += f'{"  " * (indent + 1)}Right:\n'
		s += self.right_node.to_string(indent + 2)
		return s

class UnaryOpNode(Node):
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

		self.pos_start = self.op_tok.pos_start
		self.pos_end = node.pos_end

	def __repr__(self):
		return f'UnOp({self.op_tok}, {self.node})'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}UnaryOpNode ({self.op_tok.type}):\n'
		s += f'{"  " * (indent + 1)}Operand:\n'
		s += self.node.to_string(indent + 2)
		return s

class IfNode(Node):
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case

		self.pos_start = self.cases[0][0].pos_start
		self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}IfNode:\n'
		for i, (condition, expr, result) in enumerate(self.cases):
			case_type = "If" if i == 0 else "Elif"
			s += f'{"  " * (indent + 1)}{case_type} Case:\n'
			s += f'{"  " * (indent + 2)}Condition:\n'
			s += condition.to_string(indent + 3) + '\n'
			s += f'{"  " * (indent + 2)}Body:' + '\n'
			for item in expr.element_nodes:
				s += item.to_string(indent + 3) + '\n'
			s += f'{"  " * (indent + 2)}Evaluation:\n'
			s += f'{"  " * (indent + 3)}{result}\n'
		if self.else_case:
			s += f'{"  " * (indent + 1)}Else Case:\n'
			expr, result = self.else_case
			s += f'{"  " * (indent + 2)}Body:\n'
			for item in expr.element_nodes:
				s += item.to_string(indent + 3) + '\n'
			s += f'{"  " * (indent + 2)}Evaluation:\n'
			s += f'{"  " * (indent + 3)}{result}\n'
		return s.rstrip()

class ForNode(Node):
	def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
		self.var_name_tok = var_name_tok
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.step_value_node = step_value_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.body_node.pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}ForNode (Variable: {self.var_name_tok.value}):\n'
		s += f'{"  " * (indent + 1)}Start:\n'
		s += self.start_value_node.to_string(indent + 2) + '\n'
		s += f'{"  " * (indent + 1)}End:\n'
		s += self.end_value_node.to_string(indent + 2) + '\n'
		if self.step_value_node:
			s += f'{"  " * (indent + 1)}Step:\n'
			s += self.step_value_node.to_string(indent + 2) + '\n'
		s += f'{"  " * (indent + 1)}Body:\n'
		for item in self.body_node.element_nodes:
			s += item.to_string(indent + 2)
		return s.rstrip()

class WhileNode(Node):
	def __init__(self, condition_node, body_node, should_return_null):
		self.condition_node = condition_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos_start = self.condition_node.pos_start
		self.pos_end = self.body_node.pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}WhileNode:\n'
		s += f'{"  " * (indent + 1)}Condition:\n'
		s += self.condition_node.to_string(indent + 2) + '\n'
		s += f'{"  " * (indent + 1)}Body:\n'
		for item in self.body_node.element_nodes:
			s += item.to_string(indent + 2) + '\n'
		return s.rstrip()

class FuncDefNode(Node):
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

	def to_string(self, indent=0):
		name = self.var_name_tok.value if self.var_name_tok else '<anonymous>'
		args = ', '.join([t.value for t in self.arg_name_toks])
		s = f'{"  " * indent}FuncDefNode (Name: {name}, Args: {args}, AutoReturn: {self.should_auto_return}):\n'
		s += f'{"  " * (indent + 1)}Body:\n'
		if isinstance(self.body_node, ListNode):
			for item in self.body_node.element_nodes:
				s += item.to_string(indent + 2) + '\n'
		else:
			s += f'{"  " * (indent + 2)}ReturnNode:\n'
			s += self.body_node.to_string(indent + 3) + '\n'
		return s.rstrip()

class CallNode(Node):
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes

		self.pos_start = self.node_to_call.pos_start

		if len(self.arg_nodes) > 0:
			self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
		else:
			self.pos_end = self.node_to_call.pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}CallNode:\n'
		s += f'{"  " * (indent + 1)}Function:\n'
		s += self.node_to_call.to_string(indent + 2) + '\n'
		if self.arg_nodes:
			s += f'{"  " * (indent + 1)}Arguments:\n'
			for arg in self.arg_nodes:
				s += arg.to_string(indent + 2) + '\n'
		else:
			s += f'{"  " * (indent + 1)}Arguments: None'
		return s.rstrip()

class ReturnNode(Node):
	def __init__(self, node_to_return, pos_start, pos_end):
		self.node_to_return = node_to_return

		self.pos_start = pos_start
		self.pos_end = pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}ReturnNode:\n'
		s += self.node_to_return.to_string(indent + 1)
		return s.rstrip()

class ContinueNode(Node):
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end
	
	def to_string(self, indent=0):
		return f'{"  " * indent}ContinueNode'

class BreakNode(Node):
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end

	def to_string(self, indent=0):
		return f'{"  " * indent}BreakNode'

class SwitchNode(Node):
	def __init__(self, expression_node, cases, default_case, pos_start, pos_end):
		self.expression_node = expression_node
		self.cases = cases
		self.default_case = default_case

		self.pos_start = pos_start
		self.pos_end = pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}SwitchNode:\n'
		s += f'{"  " * (indent + 1)}Condition:\n'
		s += self.expression_node.to_string(indent + 2) + '\n'
		
		s += f'{"  " * (indent + 1)}Cases:\n'
		for value, body in self.cases:
			s += f'{"  " * (indent + 2)}Case Value:\n'
			s += value.to_string(indent + 3) + '\n'
			s += f'{"  " * (indent + 2)}Case Body:\n'
			for item in body.element_nodes:
				s += item.to_string(indent + 3) + '\n'

		if self.default_case:
			s += f'{"  " * (indent + 1)}Default:\n'
			for item in self.default_case.element_nodes:
				s += item.to_string(indent + 2)
		return s.rstrip()

class TryExceptNode(Node):
	def __init__(self, try_body_node, except_body_node):
		self.try_body_node = try_body_node
		self.except_body_node = except_body_node

		self.pos_start = self.try_body_node.pos_start
		self.pos_end = self.except_body_node.pos_end

	def to_string(self, indent=0):
		s = f'{"  " * indent}TryExceptNode:\n'
		s += f'{"  " * (indent + 1)}Try Block:\n'
		for item in self.try_body_node.element_nodes:
			s += item.to_string(indent + 2) + '\n'
		s += f'{"  " * (indent + 1)}Except Block:\n'
		for item in self.except_body_node.element_nodes:
			s += item.to_string(indent + 2) + '\n'
		return s.rstrip()

class PassNode(Node):
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end

	def to_string(self, indent=0):
		return f'{"  " * indent}PassNode'

class ExitNode(Node):
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end
		sys.exit()
	
	def to_string(self, indent=0):
		return f'{"  " * indent}ExitNode'

class ImportNode(Node):
	def __init__(self, module_name_tok):
		self.module_name_tok = module_name_tok

		self.pos_start = self.module_name_tok.pos_start
		self.pos_end = self.module_name_tok.pos_end

	def to_string(self, indent=0):
		return f'{"  " * indent}ImportNode: {self.module_name_tok.value}'

class IncludeNode(Node):
	def __init__(self, module_name_tok):
		self.module_name_tok = module_name_tok

		self.pos_start = self.module_name_tok.pos_start
		self.pos_end = self.module_name_tok.pos_end

	def to_string(self, indent=0):
		return f'{"  " * indent}IncludeNode: {self.module_name_tok.value}'

class MemberAccessNode(Node):
	def __init__(self, object_node, member_name_tok):
		self.object_node = object_node
		self.member_name_tok = member_name_tok
		self.pos_start = self.object_node.pos_start
		self.pos_end = self.member_name_tok.pos_end

	def __repr__(self):
		return f'({self.object_node}.{self.member_name_tok})'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}MemberAccessNode (Member: {self.member_name_tok.value}):\n'
		s += f'{"  " * (indent + 1)}Object:\n'
		s += self.object_node.to_string(indent + 2)
		return s.rstrip()
	
class MemberAssignNode(Node):
	def __init__(self, object_node, member_name_tok, value_node):
		self.object_node = object_node
		self.member_name_tok = member_name_tok
		self.value_node = value_node
		self.pos_start = object_node.pos_start
		self.pos_end = value_node.pos_end

	def __repr__(self):
		return f'({self.object_node}.{self.member_name_tok} = {self.value_node})'
	
	def to_string(self, indent=0):
		s = f'{"  " * indent}MemberAssignNode (Member: {self.member_name_tok.value}):\n'
		s += f'{"  " * (indent + 1)}Object:\n'
		s += self.object_node.to_string(indent + 2) + '\n'
		s += f'{"  " * (indent + 1)}Value:\n'
		s += self.value_node.to_string(indent + 2)
		return s.rstrip()

class ClassDefNode(Node):
	def __init__(self, class_name_tok, method_nodes, pos_start, pos_end):
		self.class_name_tok = class_name_tok
		self.method_nodes = method_nodes
		self.pos_start = pos_start
		self.pos_end = pos_end

	def __repr__(self):
		return f'(class {self.class_name_tok.value} ...methods...)'

	def to_string(self, indent=0):
		name = self.class_name_tok.value
		s = f'{"  " * indent}ClassDefNode (Name: {name}):\n'
		s += f'{"  " * (indent + 1)}Methods:\n'
		for item in self.method_nodes:
			s += item.to_string(indent + 2) + '\n'
		return s.rstrip()