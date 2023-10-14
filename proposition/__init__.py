from utils import ChangeRepresentation

class TrueValue:
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
    
    @ChangeRepresentation
    def __add__(self, proposition) -> TrueValue:
        return TrueValue(self.value or proposition.value)
    
    @ChangeRepresentation
    def __mul__(self, proposition) -> TrueValue:
        return TrueValue(self.value and proposition.value)

    @ChangeRepresentation
    def __invert__(self) -> bool:
        return not self.value
    
    
class CompostProposition:
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

    def remove(self, element) -> None:
        self.value.remove(element)

    def append(self, element) -> None:
        self.value.append(element)

    def index(self, element) -> int:
        return self.value.index(element)
    
    def add(self, obj) -> None:
        self.value.append(obj)

    def calculate_value(self, aux=None, previous_proposition=None, **kwargs) -> bool:
        aux = aux or self
        if isinstance(aux, TrueValue):
            return aux.value
        
        for proposition in aux.value:
            if isinstance(proposition, CompostProposition):
                return self.calculate_value(aux=proposition, previous_proposition=aux, **kwargs)

        else:
            while len(aux) != 1:
                operator_index = self.find_bigger_precedence_op(aux)
                operator = aux.value[operator_index]
                aridity = self.aridity_operators[operator.__name__]

                if aridity == 2:
                    first_value = aux.value[operator_index - 1]
                    second_value = aux.value[operator_index + 1]
                    result = operator(first_value, second_value)
                    aux.remove(first_value)
                    aux.remove(operator)
                    aux.remove(second_value)
                    aux.append(result)
                
                if previous_proposition:
                    previous_proposition[previous_proposition.index(aux)] = result
                    if kwargs.get('debug'):
                        print(self)
                    return self.calculate_value(**kwargs)
                
                return result

    def find_bigger_precedence_op(self, proposition):
        bigger, operator_index = 0, 0
        for index, element in enumerate(proposition.value):
            if callable(element):
                if self.precedence_operators[element.__name__] >= bigger:
                    bigger = self.precedence_operators[element.__name__]
                    operator_index = index
                
        return operator_index