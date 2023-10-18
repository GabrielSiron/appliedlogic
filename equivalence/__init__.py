from proposition import Proposition, CompoundProposition
from utils.function_decorator import LogicOperator

class Equivalence:
    def check_distributivity(self, proposition: Proposition) -> bool:
        for index, element in enumerate(proposition):
            if isinstance(element, LogicOperator):
                return self.can_distribute(element, proposition[index + 1])

    @staticmethod
    def can_distribute(operator: LogicOperator, proposition: CompoundProposition) -> bool:
        """check if all logic operators are differents to the first operator, out of the proposition
        
        its possible use the distributive property for propositions like 'p v (p ^ q)', because the
        external and internal operators are differents. If this doenst happen, we can't use distributivity.
        This is what this function are searching for.
        """
        if isinstance(proposition, CompoundProposition):
            equal_operators = [element for element in proposition if isinstance(element, LogicOperator) and element.name == operator.name]
            if equal_operators:
                return False
            return True
        return False