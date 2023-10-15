
from proposition import Proposition, CompoundProposition

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
print(expression)
print(expression.calculate_value(debug=True))