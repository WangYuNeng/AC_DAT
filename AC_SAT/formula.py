import random

def gen_clause_uniform(k, n_var):
    vars = random.sample([i+1 for i in range(n_var)], k=k)
    signed_vars = [random.choice([1, -1]) * v for v in vars]
    return signed_vars

class Formula:

    def __init__(self, n_var=None) -> None:
        self.clauses = []
        self.var_value = []
        if n_var is not None:
            self.init_var(n_var)
        self.k = None

    def init_var(self, n_var) -> None:
        self.var_value = [False for _ in range(n_var + 1)]

    def add_clauses(self, clauses) -> None:
        self.clauses += clauses

    def set_k(self, k) -> None:
        self.k = k

    def is_sat(self) -> bool:
        for clause in self.clauses:
            unsat = True
            for var in clause:
                if self.get_var_val(var):
                    unsat = False
                    break
            if unsat:
                return False
        return True

    def n_vars(self) -> int:
        return len(self.var_value) - 1

    def n_clauses(self) -> int:
        return len(self.clauses)

    def get_var_id(self, var) -> int:
        '''
        Return the id of a variable 
        '''
        return abs(var)

    def get_var_assignment(self, var) -> bool:
        '''
        Return the original boolean value of a variable 
        '''
        return self.var_value[self.get_var_id(var)]

    def get_var_val(self, var) -> bool:
        '''
        Return the boolean value of a variable considering polarity
        '''
        if var > 0:
            return self.var_value[self.get_var_id(var)]
        else:
            return not self.var_value[self.get_var_id(var)]

    def get_var_polarity(self, var) -> bool:
        '''
        Return the polarity of a variable
        '''
        return var > 0