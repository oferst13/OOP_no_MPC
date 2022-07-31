import numpy as np

num_generations = 200
gene_space = [0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
parent_selection = "rank"

def pop_init(release_hr, n_tanks):
    num_genes = release_hr * n_tanks
    num_sols = num_genes * 2
    sol_zero = np.zeros(num_genes)
    sol_one = np.ones(num_genes) * gene_space[0]
    sol_two = np.ones(num_genes) * gene_space[1]
    sol_three = np.ones(num_genes) * gene_space[2]
    pre_det = np.array([sol_zero,
                       sol_one,
                       sol_two,
                       sol_three])
    rest = np.random.randint(11, size=(num_sols - np.shape(pre_det)[0], num_genes))
    initial_pop = np.concatenate((pre_det, rest), axis=0)
    return initial_pop
