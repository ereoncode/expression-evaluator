# expression_evaluator
Simple Expression Evaluator based on "Python Cookbook" recipes.
Recursive descent parser.

Grammar:
```
expression ::= {'-'}* term { ('+'|'-') term }*
term ::= factor { ('*'|'/'|'%'|'//'|'**') factor }*
factor ::= (INT | FLOAT) | (expr)
```

Usage:

```python
>>>e = ExpressionEvaluator()
>>>print(e.parse('2 * 3 + (1 / 5) * (-1)')
5.8
```
