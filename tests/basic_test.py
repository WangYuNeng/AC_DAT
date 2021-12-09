from AC_SAT.manager import Manager
from AC_SAT.acsat import AC_solver

if __name__ == "__main__":
    mgr = Manager()
    solver = AC_solver()

    mgr.generate_random_ksat_formula(3, 5, 4)
    mgr.solve(solver=solver)