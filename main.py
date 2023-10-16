
from proposition import Proposition, CompoundProposition
from copy import copy, deepcopy

p = Proposition(text='p', value=True)
q = Proposition(text='q', value=True)

print(f'p é {p.value}')
print(f'q é {q.value}')

expression = CompoundProposition()
expression.add(p)
expression.add(p.__add__)
negation = CompoundProposition()
negation.add(p.__invert__)
negation.add(p)
expression.add(negation)
expression2 = copy(expression)
expression2.value = deepcopy(expression.value)
print(expression2)
# COPY THE LIST INSIDE EXPRESSION, NOT ONLY EXPRESSION. THE REFERENCES INSIDE EXPRESSION KEEP THE SAME AFTER COPY()
expression2.prepare_calculus()
print(expression2.calculate_value(debug=True))
expression2.prepare_calculus()
print(expression2.calculate_value(debug=True))