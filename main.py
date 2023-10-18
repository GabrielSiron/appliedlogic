from proposition import Proposition, CompoundProposition

p = Proposition(text='p', value=True)
q = Proposition(text='q', value=True)
p_or_q = CompoundProposition([p, p.__add__, p])
p_and_q = CompoundProposition([p, p.__mul__, p])
proposition = CompoundProposition([p_or_q, p.__add__, p_and_q])
proposition.prepare_calculus()
print(proposition.calculate_value())