from test_maps import *
from test_movies import *
import sys

obs_name = 'RM'
par_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
par_rng = np.linspace(-100, 100, 201)
boundary = None  # Set to None for no boundaries

if __name__ == "__main__":
    i = int(sys.argv[1])-1
    # Make pictures, plots, figures, maps, etc.
    for par_val in par_rng:
        generate_mapplot(obs_name, par_num[i], par_rng, par_val, boundary)
    generate_movie(obs_name, par_num[i], par_rng)
