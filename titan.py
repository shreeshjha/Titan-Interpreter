INTEGER, PLUS, MINUS, MULTIPLICATION, DIVISON, LPAREN, RPAREN,  EOF = ('INTEGER', 'PLUS', 'MINUS','MUL', 'DIV', '(', ')', 'EOF')

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, statement):
        
        self.statement = statement
        # self.pos is an index into self.statement
        self.pos = 0
        self.current_char = self.statement[self.pos]

    def error(self):
        raise Exception('Character Not Valid :( ')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.statement) - 1:
            self.current_char = None 
        else:
            self.current_char = self.statement[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLICATION, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVISON, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def proces(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.proces(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.proces(LPAREN)
            node = self.expr()
            self.proces(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MULTIPLICATION, DIVISON):
            token = self.current_token
            if token.type == MULTIPLICATION:
                self.proces(MULTIPLICATION)
            elif token.type == DIVISON:
                self.proces(DIVISON)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.proces(PLUS)
            elif token.type == MINUS:
                self.proces(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()


class NodeVis(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Titan(NodeVis):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MULTIPLICATION:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIVISON:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            try:
                statement = input('titan -> ')
            except NameError:
                statement = input('titan -> ')
        except EOFError:
            break
        if not statement:
            continue

        lexer = Lexer(statement)
        parser = Parser(lexer)
        titan = Titan(parser)
        result = titan.interpret()
        print(result)


if __name__ == '__main__':
    main()