class Node:
    """Узел односвязного списка."""
    def __init__(self, coef=0, deg=0):
        self.coef = coef
        self.deg = deg
        self.next = None

class Polynomial:
    """Односвязный список для многочлена."""
    
    def __init__(self):
        self.head = None

    def add_term(self, coef, deg):
        """Добавляет член с объединением подобных"""
        if coef == 0:
            return
            
        current = self.head
        prev = None
        
        while current is not None:
            if current.deg == deg:
                current.coef += coef
                if current.coef == 0:
                    if prev is None:
                        self.head = current.next
                    else:
                        prev.next = current.next
                return
            prev = current
            current = current.next
        
        new_node = Node(coef, deg)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def add_term_raw(self, coef, deg):
        new_node = Node(coef, deg)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

def input_polynomial(expr):
    """Ввод: из строки в список."""
    poly = Polynomial()
    expr = expr.replace(" ", "")
    
    if not expr:
        return poly
    
    if expr[0] not in '+-':
        expr = '+' + expr
    
    i = 0
    n = len(expr)
    
    while i < n:
        if expr[i] == '+':
            sign = 1
            i += 1
        elif expr[i] == '-':
            sign = -1
            i += 1
        else:
            sign = 1
        
        if i >= n:
            raise ValueError("После знака '" + ('+' if sign == 1 else '-') + "' ничего нет")
        
        coef = 0
        has_coef = False
        while i < n and expr[i].isdigit():
            coef = coef * 10 + int(expr[i])
            has_coef = True
            i += 1
        
        if not has_coef:
            coef = 1
        coef *= sign
        
        deg = 0
        if i < n and expr[i] == 'y':
            i += 1
            if i < n and expr[i] == '^':
                i += 1
                if i >= n:
                    raise ValueError("После '^' нет степени")
                deg = 0
                while i < n and expr[i].isdigit():
                    deg = deg * 10 + int(expr[i])
                    i += 1
            else:
                deg = 1
        else:
            deg = 0
        
        poly.add_term_raw(coef, deg)
    
    return poly


def output_polynomial(poly):
    if poly is None or poly.head is None:
        return "0"
    
    result = []
    current = poly.head
    
    while current is not None:
        coef = current.coef
        deg = current.deg
        
        if coef == 0:
            current = current.next
            continue
        
        if deg == 0:
            term = str(coef)
        else:
            if coef == 1:
                term = "y"
            elif coef == -1:
                term = "-y"
            else:
                term = str(coef) + "y"
            if deg > 1:
                term += "^" + str(deg)
        
        result.append(term)
        current = current.next
    
    if not result:
        return "0"
    
    output = result[0]
    for term in result[1:]:
        if term[0] == '-':
            output += term
        else:
            output += '+' + term
    
    return output


def simplify_polynomial(poly):
    if poly is None or poly.head is None:
        return poly
    
    coeffs = {}
    current = poly.head
    
    while current is not None:
        deg = current.deg
        if deg in coeffs:
            coeffs[deg] += current.coef
        else:
            coeffs[deg] = current.coef
        current = current.next
    
    to_delete = []
    for deg in coeffs:
        if coeffs[deg] == 0:
            to_delete.append(deg)
    for deg in to_delete:
        del coeffs[deg]
    
    if not coeffs:
        empty_poly = Polynomial()
        empty_poly.add_term_raw(0, 0)
        return empty_poly
    
    sorted_degrees = list(coeffs.keys())
    n = len(sorted_degrees)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_degrees[j] < sorted_degrees[j + 1]:
                sorted_degrees[j], sorted_degrees[j + 1] = sorted_degrees[j + 1], sorted_degrees[j]
    
    new_poly = Polynomial()
    for deg in sorted_degrees:
        new_poly.add_term(coeffs[deg], deg)
    
    return new_poly


def validate_expression(expr):
    """Проверяет корректность выражения."""
    if not expr:
        return False, "Выражение пустое"
    
    for ch in expr:
        if ch == ' ':
            continue
        if ch.isdigit():
            continue
        if ch in '+-^yY':
            continue
        return False, "Недопустимый символ '" + ch + "'"
    
    return True, ""


def read_from_file(filename="input.txt"):
    """Читает многочлен из файла."""
    try:
        f = open(filename, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        
        if not lines:
            return None, "Файл пуст."
        
        expr = lines[0].strip()
        if not expr:
            return None, "Первая строка пуста."
        
        is_valid, error_msg = validate_expression(expr)
        if not is_valid:
            return None, error_msg
        
        poly = input_polynomial(expr)
        if poly is None or poly.head is None:
            return None, "Не удалось распознать многочлен."
        
        return poly, None
        
    except FileNotFoundError:
        return None, "Файл не найден."
    except Exception as e:
        return None, str(e)


def save_to_file(poly, filename="input.txt"):
    """Сохраняет результат в конец файла."""
    if poly is None:
        return False, "Многочлен пуст."
    
    result_str = output_polynomial(poly)
    
    try:
        f = open(filename, 'a', encoding='utf-8')
        f.write("\nРезультат после приведения подобных:\n")
        f.write(result_str + "\n")
        f.close()
        return True, "Результат успешно сохранен"
    except Exception as e:
        return False, "Ошибка при сохранении: " + str(e)
