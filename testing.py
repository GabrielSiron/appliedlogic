import unittest
from proposition import Proposition, CompoundProposition, TruthValue
from equivalence import Equivalence

class TestCalculusOfTruthValue(unittest.TestCase):
    def test_keep_the_truth_value(self):
        p = Proposition(text='p', value=True)
        proposition = CompoundProposition()
        proposition.add(p)
        proposition.prepare_calculus()
        self.assertEqual(proposition.calculate_value(p), True)

    def test_tautologies(self):
        truth_values = [True, False]

        for truth_value in truth_values:
            p = Proposition(text='p', value=truth_value)
            proposition = CompoundProposition()
            not_p = CompoundProposition()
            not_p.create([p.__invert__, p])
            proposition.create([p, p.__add__, not_p])
            proposition.prepare_calculus()
            self.assertEqual(proposition.calculate_value(), True)

    def test_contradictions(self):
        truth_values = [True, False]

        for truth_value in truth_values:
            p = Proposition(text='p', value=truth_value)
            proposition = CompoundProposition()
            not_p = CompoundProposition()
            not_p.create([p.__invert__, p])
            proposition.create([p, p.__mul__, not_p])
            proposition.prepare_calculus()
            self.assertEqual(proposition.calculate_value(), False)

    def test_existing_distributivity_pattern(self):
        p = Proposition(text='p')
        q = Proposition(text='q')
        proposition = CompoundProposition([p, p.__add__, CompoundProposition([p, p.__mul__, q])])
        tester = Equivalence()
        self.assertEqual(tester.check_distributivity(proposition), True)

    def test_non_existing_distributive_pattern(self):
        p = Proposition(text='p')
        q = Proposition(text='q')
        proposition = CompoundProposition([p, p.__mul__, q])
        tester = Equivalence()
        self.assertEqual(tester.check_distributivity(proposition), False)
        
if __name__ == '__main__':
    unittest.main() 