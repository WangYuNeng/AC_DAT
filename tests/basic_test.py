import random
import time
import os
from tqdm import tqdm

from AC_SAT.manager import Manager
from AC_SAT.acsat import AC_solver

if __name__ == "__main__":
    mgr = Manager()
    solver = AC_solver()

    random.seed(428)
    k = 3
    min_var, max_var = 3, 11
    min_alpha, max_alpha = 1, 8
    n_round = 428
    tmp_dir = "tmp_{}".format(int(time.time()))
    os.mkdir(tmp_dir)
    for alpha in range(min_alpha, max_alpha):
        alpha_dir = os.path.join(tmp_dir, "{}".format(alpha))
        os.mkdir(alpha_dir)
        
        for n_vars in range(min_var, max_var):
            n_clauses = n_vars * alpha
            var_dir = os.path.join(alpha_dir, "{}".format(n_vars))
            os.mkdir(var_dir)
            print("alpha={}, n_clauses={}, n_vars={}".format(alpha, n_clauses, n_vars))
            for trial in tqdm(range(n_round)):
                mgr.generate_random_ksat_formula(k, n_clauses, n_vars)
                is_sat = mgr.solve(solver=solver)
                save_path = os.path.join(var_dir, "{}_{}".format(is_sat, n_round))
                solver.plot_sol(save_path)