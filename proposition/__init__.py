from copy import deepcopy
from utils.function_decorator import ChangeRepresentation

class TruthValue:
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)
    
class Proposition:
    def __init__(self, text, value=False) -> None:
        self.text = text
        self.value = value

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return str(self)
    
    @staticmethod
    @ChangeRepresentation
    def __add__(left_proposition, right_proposition) -> TruthValue:
        return TruthValue(left_proposition.value or right_proposition.value)
    
    @staticmethod
    @ChangeRepresentation
    def __mul__(left_proposition, right_proposition) -> TruthValue:
        return TruthValue(left_proposition.value and right_proposition.value)

    @staticmethod
    @ChangeRepresentation
    def __invert__(proposition) -> bool:
        return TruthValue(not proposition.value)
    
    
class CompoundProposition:
    def __init__(self) -> None:
        self.precedence_operators = {
            '__add__': 0,
            '__mul__': 0,
            '__invert__': 1
        }

        self.aridity_operators = {
            '__add__': 2,
            '__mul__': 2,
            '__invert__': 1
        }

        self.value = []

    def __str__(self) -> str:
        return str(self.value).replace('[', '(').replace(']', ')').replace(',', ' ')
    
    def __setitem__(self, index, element) -> None:
        self.value[index] = element

    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self) -> int:
        return len(self.value)

    def pop(self, element) -> None:
        self.value.pop(element)

    def prepare_calculus(self) -> None:
        self.copy_value = deepcopy(self.value)

    def remove(self, element) -> None:
        self.value.remove(element)

    def append(self, element) -> None:
        self.value.append(element)

    def create(self, elements):
        self.value.extend(elements)

    def index(self, element) -> int:
        return self.value.index(element)
    
    def add(self, obj) -> None:
        self.value.append(obj)

    @staticmethod
    def do_operation(logical_operator, aridity, propositions):
        if aridity == 1: return logical_operator(propositions[0])
        return logical_operator(propositions[0], propositions[1])    
    
    @staticmethod
    def find_compound_propositions(compound_proposition):
        compound_propositions = [x for x in compound_proposition.value if isinstance(x, CompoundProposition)]
        if compound_propositions:
            return compound_propositions[0]
        
        return False

    @staticmethod
    def organizing_proposition(compound_proposition, new_value, first_index, remove_count):
        for _ in range(remove_count):
            compound_proposition.pop(first_index)

        compound_proposition.append(new_value)

    @staticmethod
    def separeting_components(compound_proposition, operator_index, aridity):
        if aridity == 1:
            return compound_proposition[operator_index - 1], compound_proposition[operator_index + 1]
        
        return compound_proposition[operator_index + 1]
    
    def calculate_value(self, propositions=None, previous_proposition=None, **kwargs) -> bool:

        propositions = self if not propositions else propositions
        
        if not isinstance(propositions, CompoundProposition):
            return propositions.value
        
        proposition = self.find_compound_propositions(propositions)

        if proposition:
            return self.calculate_value(propositions=proposition, previous_proposition=propositions, **kwargs)

        result = None

        while len(propositions) != 1:
            operator_index, operator = self.find_bigger_precedence_op(propositions)
            aridity = self.aridity_operators[operator.__name__]

            if aridity == 1:
                proposition = propositions.value[operator_index + 1]
                result = self.do_operation(operator, aridity, (proposition,))
            
            elif aridity == 2:
                left_proposition = propositions.value[operator_index - 1]
                right_proposition = propositions.value[operator_index + 1]
                result = self.do_operation(operator, aridity, (right_proposition, left_proposition))
            
            self.organizing_proposition(propositions, result, first_index=operator_index - 1, remove_count=aridity + 1)
             
        if previous_proposition:
            previous_proposition[previous_proposition.index(propositions)] = result
            return self.calculate_value(**kwargs)

        if result:
            self.value = self.copy_value
            return result.value

    def find_bigger_precedence_op(self, proposition):
        bigger, operator_index = 0, 0
        for index, element in enumerate(proposition.value):
            if callable(element):
                if self.precedence_operators[element.__name__] >= bigger:
                    bigger = self.precedence_operators[element.__name__]
                    operator_index = index
        
        return operator_index, proposition.value[operator_index]