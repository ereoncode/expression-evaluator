# -*- coding: utf-8 -*-

import re
import collections

NUM = r'(?P<NUM>\d+(\.\d+)*)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>\-)'
POW = r'(?P<POW>\*{2})'
FLOORDIV = r'(?P<FLOORDIV>/{2})'
MODULE = r'(?P<MODULE>\%)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

pattern = re.compile('|'.join([NUM, PLUS, MINUS, POW, MODULE, FLOORDIV, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

Token = collections.namedtuple('Token', ['type', 'value'])


def _tokenize(text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        token = Token(m.lastgroup, m.group())
        if token.type != 'WS':
            yield token


class ExpressionEvaluator:
    """
        Implementation of a recursive descent parser.
    Each method implements a single grammar rule. Use the ._accept() method
    to test and accept the current lookahead token. Use the ._expect()
    method to exactly match and discard the next token on on the input
    (or raise a SyntaxError if it doesn't match).

    Grammar rules:
        expression ::=  term { ('+'|'-') term }*
        term ::= factor { ('*'|'/'|'%'|'//'|'**') factor }*
        factor ::= {'-'}* NUM | (expr)
    """

    def __init__(self):
        self.tokens = None
        self.token = None
        self.next_token = None

    def parse(self, text: str):
        self.tokens = _tokenize(text)
        self.token = None
        self.next_token = None
        self._advance()
        return self.expression()

    def _advance(self):
        """Advance one token ahead"""
        self.token, self.next_token = self.next_token, next(self.tokens, None)

    def _accept(self, toktype: str):
        """Test and consume the next token if it matches toktype"""
        if self.next_token and self.next_token.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _accept_many(self, types_list):
        """Test and consume the next token if it matches toktype list"""
        if self.next_token and self.next_token.type in types_list:
            self._advance()
            return True
        else:
            return False

    def _expect(self, token_type):
        """Consume next token if it matches token_type or raise SyntaxError"""
        if not self._accept(token_type):
            raise SyntaxError('Expected ' + token_type)

    def expression(self):
        """ expression ::= term { ('+'|'-') term }* """
        expression_value = self.term()

        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.token.type
            right = self.term()
            if op == 'PLUS':
                expression_value += right
            elif op == 'MINUS':
                expression_value -= right
            else:
                raise SyntaxError(f'Unsupported operator: {op}')

        return expression_value

    def term(self):
        """ term ::= factor { ('*'|'/'|'%'|'//'|'**') factor }* """

        term_value = self.factor()
        while self._accept_many(['TIMES', 'DIVIDE', 'POW', 'MODULE', 'FLOORDIV']):
            op = self.token.type
            right = self.factor()
            if op == 'TIMES':
                term_value *= right
            elif op == 'DIVIDE':
                term_value /= right
            elif op == 'POW':
                term_value **= right
            elif op == 'MODULE':
                term_value %= right
            elif op == 'FLOORDIV':
                term_value //= right
            else:
                raise SyntaxError(f'Unsupported operator: {op}')

        return term_value

    def factor(self):
        """ factor ::= {'-'}* NUM | (expr) """
        sign = int(not self._accept('MINUS')) * 2 - 1

        if self._accept('NUM'):
            return int(self.token.value) * sign
        elif self._accept('LPAREN'):
            expression_value = self.expression() * sign
            self._expect('RPAREN')
            return expression_value
        else:
            raise SyntaxError('Expected NUM, RPAREN or LPAREN')


class ExpressionTreeBuilder(ExpressionEvaluator):
    def expression(self):
        """ expression ::= term { ('+'|'-') term }* """
        expression_value = self.term()

        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.token.type
            right = self.term()
            if op == 'PLUS':
                expression_value = ('+', expression_value, right)
            elif op == 'MINUS':
                expression_value = ('-', expression_value, right)
        return expression_value

    def term(self):
        """ term ::= factor { ('*'|'/'|'%'|'//'|'**') factor }* """

        term_value = self.factor()
        while self._accept_many(['TIMES', 'DIVIDE', 'POW', 'MODULE', 'FLOORDIV']):
            op = self.token.type
            right = self.factor()
            if op == 'TIMES':
                term_value = ('*', term_value, right)
            elif op == 'DIVIDE':
                term_value = ('/', term_value, right)
            elif op == 'POW':
                term_value = ('**', term_value, right)
            elif op == 'MODULE':
                term_value = ('%', term_value, right)
            elif op == 'FLOORDIV':
                term_value = ('//', term_value, right)
        return term_value

    def factor(self):
        """ factor ::= {'-'}* NUM | (expr) """
        sign = int(not self._accept('MINUS')) * 2 - 1

        if self._accept('NUM'):
            if sign < 0:
                return '*', -1, int(self.token.value)
            else:
                return int(self.token.value)
        elif self._accept('LPAREN'):
            expression_value = self.expression()
            self._expect('RPAREN')
            if sign < 0:
                return '*', -1, expression_value
            else:
                return expression_value
        else:
            raise SyntaxError('Expected NUM, RPAREN or LPAREN')
