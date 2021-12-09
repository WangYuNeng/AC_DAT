import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from AC_SAT.formula import Formula

def formula_dynamics(t, vars: np.ndarray, c: np.ndarray, n_clauses, n_vars, k):
    s = vars[:n_vars]
    a = vars[n_vars:]
    Ks = [
        (2 ** -k) * np.prod([1- c[m, i] * s[i] for i in range(n_vars)]) 
        for m in range(n_clauses)
    ]
    dsdt = [
        np.sum([2 * a[m] * c[m, i] * Ks[m] * Ks[m] / (1 - c[m,i] * s[i]) for m in range(n_clauses)]) 
        for i in range(n_vars)
    ]
    dadt = [a[m] * Ks[m] for m in range(n_clauses)]
    return dsdt + dadt


class AC_solver:
    '''
    Implement a dynamical system to solve SAT formula
    '''

    def __init__(self, t_span=[0, 50]) -> None:
        self.t_span = t_span
        pass

    def solve(self, formula: Formula):
        n_vars = formula.n_vars()
        n_clauses = formula.n_clauses()
        val_at_0 = [0 for _ in range(n_vars)] + [1 for _ in range(n_clauses)]
        c = np.zeros(shape=(n_clauses, n_vars))
        for m, clause in enumerate(formula.clauses):
            for var in clause:
                if var > 0:
                    c[m, var - 1] = 1
                else:
                    c[m, -var - 1] = -1
        k = formula.k
        sol = solve_ivp(formula_dynamics, self.t_span, val_at_0, args=(c, n_clauses, n_vars, k))

        s = sol.y[:n_vars:, -1]
        for i in range(n_vars):
            if s[i] > 0:
                formula.var_value[i+1] = True
            else:
                formula.var_value[i+1] = False
        return formula.is_sat()