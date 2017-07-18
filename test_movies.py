import imageio
import distutils.dir_util

# If no directory exists for the made movies and plots, make one
distutils.dir_util.mkpath('movies')


# Generates a .mp4-file containing a slideshow of all combined figures
def generate_movie(obs_name, par_num, par_rng, slowdown=False):
    """
    Generates a .mp4-file which contains a slideshow of all combined figures
    made with test_maps.py. Optionally, the slideshow can be slowed down in the
    center.

    Parameters
    ----------
    obs_name : 'RM'
        Acronym of observable name. Only 'RM' is supported right now.
    par_num : int
        Number of parameter corresponding to the index of parameter in
        Hammurabi.
    par_rng : :mod:`~numpy.ndarray`
        Range of carrier mapper values for which the likelihood needs to be
        calculated.
    slowdown : bool; optional. Default: False
        Where or not to slow down the slideshow in the center of the likelihood
        plot.

    Returns
    -------
    out : .mp4-file
        .mp4-file containing the slideshow.

    """

    # Make an array containing the filenames of all required combined figures
    filenames = []

    # If no slowdown is present, write all of them down once
    if slowdown is False:
        for par_val in par_rng:
            filenames.append('movies/rm_com_p%s_v%s.png' % (par_num, par_val))

    # If slowdown is present, write some filenames down more than once
    elif slowdown is True:
        for par_val in par_rng:
            filenames.append('movies/rm_com_p%s_v%s.png' % (par_num, par_val))
            if(15 < abs(par_val) <= 20):
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
            if(10 < abs(par_val) <= 15):
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
            if(5 < abs(par_val) <= 10):
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
            if(0 <= abs(par_val) <= 5):
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))
                filenames.append('movies/rm_com_p%s_v%s.png'
                                 % (par_num, par_val))

    # Make an array containing the images and fill it
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))

    # Save the slideshow
    if slowdown is False:
        imageio.mimsave('movies/rm_movie_p%s.mp4' % (par_num), images)
    elif slowdown is True:
        imageio.mimsave('movies/rm_movie_p%s_slowed.mp4' % (par_num), images)
