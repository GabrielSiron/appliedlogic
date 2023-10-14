
from proposition import Proposition, CompostProposition

p = Proposition(text='p', value=True)
q = Proposition(text='q', value=True)

print(f'p é {p.value}')
print(f'q é {q.value}')

expression = CompostProposition()
expression.add(p)
expression.add(p.__mul__)
expression.add(q)
# expression2 = CompostProposition()
# expression2.add(p)
# expression2.add(p.__mul__)
# expression2.add(q)
# expression.add(expression2)
print(expression)
print(expression.calculate_value(debug=True))