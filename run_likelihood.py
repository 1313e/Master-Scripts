from test_likelihood import *
import sys

obs_name = 'RM'
par_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
par_rng = np.linspace(-100, 100, 201)

if __name__ == "__main__":
    i = int(sys.argv[1])-1
    calc_likelihood(par_num[i], par_rng)
    plot_likelihood(par_num[i], par_rng)
