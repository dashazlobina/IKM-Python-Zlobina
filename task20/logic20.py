class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.is_unary = False


def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    
    while i < n:
        ch = expr[i]
        
        if ch == ' ':
            i += 1
            continue
        
        if ch.isdigit():
            num = ''
            while i < n and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append(num)
            continue
        
        if ch.isalpha():
            tokens.append(ch)
            i += 1
            continue
        
        if ch in '+-*/()':
            tokens.append(ch)
            i += 1
            continue
        
        i += 1
    
    return tokens


def parse_expression(tokens, pos):
    node, pos = parse_term(tokens, pos)
    
    while pos < len(tokens) and tokens[pos] in '+-':
        op = tokens[pos]
        pos += 1
        right, pos = parse_term(tokens, pos)
        node = Node(op, node, right)
    
    return node, pos


def parse_term(tokens, pos):
    node, pos = parse_factor(tokens, pos)
    
    while pos < len(tokens) and tokens[pos] in '*/':
        op = tokens[pos]
        pos += 1
        right, pos = parse_factor(tokens, pos)
        node = Node(op, node, right)
    
    return node, pos


def parse_factor(tokens, pos):
    if pos >= len(tokens):
        return None, pos
    
    token = tokens[pos]
    
    if token == '-':
        pos += 1
        node, pos = parse_factor(tokens, pos)
        if node is not None:
            unary_node = Node('-', node, None)
            unary_node.is_unary = True
            return unary_node, pos
        return None, pos
    
    if token == '(':
        pos += 1
        node, pos = parse_expression(tokens, pos)
        if pos < len(tokens) and tokens[pos] == ')':
            pos += 1
            return node, pos
        return None, pos
    
    if token.isdigit():
        return Node(token), pos + 1
    
    if token.isalpha():
        if pos + 1 < len(tokens) and tokens[pos + 1].isalpha():
            return None, pos
        return Node(token), pos + 1
    
    return None, pos


def build_tree(expr):
    tokens = tokenize(expr)
    if not tokens:
        return None
    
    tree, pos = parse_expression(tokens, 0)
    
    if pos < len(tokens):
        return None
    
    return tree


def tree_to_string(node):
    if node is None:
        return ""
    
    if node.left is None and node.right is None:
        return str(node.value)
    
    if node.is_unary:
        return "(-" + tree_to_string(node.left) + ")"
    
    left_str = tree_to_string(node.left)
    right_str = tree_to_string(node.right)
    
    return "(" + left_str + " " + node.value + " " + right_str + ")"


def is_multiplication(node):
    return node is not None and node.value == '*' and not node.is_unary


def is_addition(node):
    return node is not None and node.value == '+' and not node.is_unary


def simplify_distributive(node):
    if node is None:
        return None
    
    node.left = simplify_distributive(node.left)
    node.right = simplify_distributive(node.right)
    
    if is_addition(node):
        left = node.left
        right = node.right
        
        if is_multiplication(left) and is_multiplication(right):
            if left.right is not None and right.right is not None:
                if str(left.right.value) == str(right.right.value):
                    f1 = left.left
                    f2 = right.left
                    f3 = left.right
                    
                    sum_node = Node('+', f1, f2)
                    new_node = Node('*', sum_node, f3)
                    return simplify_distributive(new_node)
        
        if is_multiplication(left) and is_multiplication(right):
            if left.left is not None and right.left is not None:
                if str(left.left.value) == str(right.left.value):
                    f1 = left.left
                    f2 = left.right
                    f3 = right.right
                    
                    sum_node = Node('+', f2, f3)
                    new_node = Node('*', f1, sum_node)
                    return simplify_distributive(new_node)
    
    return node


def simplify_tree(node):
    return simplify_distributive(node)
