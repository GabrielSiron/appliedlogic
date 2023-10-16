from proposition import Proposition, CompoundProposition

p = Proposition(text='p', value=True)
q = Proposition(text='q', value=True)

negation_value = [p.__invert__, p]
negation_p = CompoundProposition(negation_value)
proposition_value = [p, p.__add__, negation_p]
proposition = CompoundProposition(proposition_value)
proposition.prepare_calculus()
print(proposition.calculate_value())