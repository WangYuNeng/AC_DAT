import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from AC_SAT.formula import Formula

def calc_Km(c, s, k):
    (n_clauses, n_vars) = c.shape
    ret = [
        (2 ** -k) * np.prod([1- c[m, i] * s[i] for i in range(n_vars)]) 
        for m in range(n_clauses)
    ]
    return ret

def calc_Kmi(c, s, k):
    (n_clauses, n_vars) = c.shape
    ret = np.zeros(shape=[n_clauses, n_vars])
    for m in range(n_clauses):
        tmp_at_m = [1- c[m, i] * s[i] for i in range(n_vars)]
        for i in range(n_vars):
            tmp_at_mi = tmp_at_m.copy()
            tmp_at_mi[i] = 1
            ret[m, i] = (2 ** -k) * np.prod(tmp_at_mi)
    return ret

def calc_dsdt(Km, Kmi, a, c):
    (n_clauses, n_vars) = c.shape
    ret = [
        np.sum([2 * a[m] * c[m, i] * Km[m] * Kmi[m, i] for m in range(n_clauses)]) 
        for i in range(n_vars)
    ]
    return ret

def calc_dadt(Km, a):
    ret = [am * kmm for am, kmm in zip(a, Km)]
    return ret

def calc_c(formula):
    n_vars = formula.n_vars()
    n_clauses = formula.n_clauses()
    c = np.zeros(shape=(n_clauses, n_vars))
    for m, clause in enumerate(formula.clauses):
        for var in clause:
            if var > 0:
                c[m, var - 1] = 1
            else:
                c[m, -var - 1] = -1
    return c

def formula_dynamics(t, vars: np.ndarray, c: np.ndarray, n_clauses, n_vars, k):
    s = vars[:n_vars]
    a = vars[n_vars:]
    Km = calc_Km(c, s, k)
    Kmi = calc_Kmi(c, s, k)
    dsdt = calc_dsdt(Km, Kmi, a, c)
    dadt = calc_dadt(Km, a)
    return dsdt + dadt


class AC_solver:
    '''
    Implement a dynamical system to solve SAT formula
    '''

    def __init__(self, t_span=[0, 50]) -> None:
        self.t_span = t_span
        self.formula = None
        self.sol = None

    def solve(self, formula: Formula):
        n_vars = formula.n_vars()
        n_clauses = formula.n_clauses()
        val_at_0 = [0 for _ in range(n_vars)] + [1 for _ in range(n_clauses)]
        c = calc_c(formula)
        k = formula.k
        sol = solve_ivp(formula_dynamics, self.t_span, val_at_0, args=(c, n_clauses, n_vars, k), dense_output=True)

        s = sol.y[:n_vars:, -1]
        for i in range(n_vars):
            if s[i] > 0:
                formula.var_value[i+1] = True
            else:
                formula.var_value[i+1] = False

        self.formula = formula
        self.sol = sol
        return formula.is_sat()

    def plot_sol(self, save_path):
        assert self.formula is not None
        assert self.sol is not None

        n_vars = self.formula.n_vars()
        n_clauses = self.formula.n_clauses()
        t = np.linspace(*(self.t_span), 300)
        z = self.sol.sol(t)
        s_arr = z[:n_vars].T
        a_arr = z[n_vars:].T

        c = calc_c(self.formula)
        k = self.formula.k
        Km_arr = np.array([calc_Km(c, s, k) for s in s_arr])
        Kmi_arr = np.array([calc_Kmi(c, s, k) for s in s_arr])
        dsdt_arr = np.array([
            calc_dsdt(Km, Kmi, a, c) 
            for Km, Kmi, a in zip(Km_arr, Kmi_arr, a_arr)
        ])
        dadt_arr = np.array([
            calc_dadt(Km, a) 
            for Km, a in zip(Km_arr, a_arr)
        ])
        V_arr = np.array([np.dot(a, np.square(Km)) 
            for Km, a in zip(Km_arr, a_arr)
        ])
        plt.gcf().set_size_inches(7, 15)
        plt.subplot(611)
        plt.gca().set_title('s')
        plt.plot(t, s_arr)
        plt.subplot(612)
        plt.gca().set_title('dsdt')
        plt.plot(t, dsdt_arr)
        plt.subplot(613)
        plt.gca().set_title('a')
        plt.plot(t, a_arr)
        plt.subplot(614)
        plt.gca().set_title('dadt')
        plt.plot(t, dadt_arr)
        plt.subplot(615)
        plt.gca().set_title('Km')
        plt.plot(t, Km_arr)
        plt.subplot(616)
        plt.gca().set_title('V')
        plt.plot(t, V_arr)
        plt.xlabel('t')
        plt.savefig(save_path)
        plt.clf()