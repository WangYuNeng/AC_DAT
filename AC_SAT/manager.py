from scipy.integrate._ivp.ivp import solve_ivp
from AC_SAT.formula import Formula, gen_clause_uniform

class Manager:

    def __init__(self) -> None:
        pass

    def read_DIMACS(self, file_name: str) -> None:
        pass

    def solve(self, solver: object) -> None:
        return solver.solve(self.formula)

    def generate_random_ksat_formula(self, k, n_clauses, n_vars) -> None:
        self.formula = Formula()
        self.formula.init_var(n_vars)
        clauses = [gen_clause_uniform(k, n_vars) for _ in range(n_clauses)]
        self.formula.add_clauses(clauses)
        self.formula.set_k(k)
        
