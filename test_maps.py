from imagine import *
from nifty import *
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import distutils.dir_util

hammu12 = Hammurapy_jf12(350, 350, random_disk_field_falloff='1/r',
                         hammurabi_path='/home/gvelden/imagine_downloads/'
                                        'hammurabi_3')
h = hp_space(int(hammu12.get_default_parameters_dict()['obs_NSIDE']))

# If no directory exists for the made movies and plots, make one
distutils.dir_util.mkpath('movies')


# Generates a combined mapplot for a given parameter number and range
def generate_mapplot(obs_name, par_num, par_rng, par_val, boundary):
    """
    For a given observable name, parameter number, carrier mapper-range,
    parameter value and observable range, generates the following maps:
    An observable map with specified boundaries.
    A likelihood plot with a cross at the specified parameter value.
    A combined figure containing both plots.

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
    par_val : float
        Value of specified parameter
    boundary : int, float or None
        If int or float, generates observable map with specified boundaries.

        If *None*, generates observable map with no variable boundaries.

    Returns
    -------
    out : Multiple .png-files
        .png-files containing the three different figures.

    """

    parameters = [0]*hammu12.get_parameter_dimension()
    parameters[par_num] = par_val

    obs = hammu12.calc_observables(parameters)

    if(obs_name == 'RM'):
        # Make observable map with defined boundary-type
        if boundary is None:
            field(h, val=obs['rm_observable']['rm_map']).plot(save='movies/rm_map_p%s_v%s.png' % (par_num, par_val), title='RM Map of Parameter %s: %s, at value %s' % (par_num, hammu12.jf12_parameter_names[par_num], par_val), unit='Rotation Measure $[\mathrm{rad/m^2}]$')
        elif(type(boundary) == int or type(boundary) == float):
            field(h, val=obs['rm_observable']['rm_map']).plot(save='movies/rm_map_p%s_v%s.png' % (par_num, par_val), title='RM Map of Parameter %s: %s, at value %s' % (par_num, hammu12.jf12_parameter_names[par_num], par_val), unit='Rotation Measure $[\mathrm{rad/m^2}]$', vmin=-1*boundary, vmax=boundary)
        else:
            raise ValueError("ERROR: Unknown boundary type")

        # Save the raw-data of observable map in a .npy-file
        np.save('movies/rm_map_p%s_v%s' % (par_num, par_val), obs['rm_observable']['rm_map'])

        # Load previously generated likelihood data
        likelihoods = np.load('data%s_RM.npy' % (par_num))

        # Make and save a likelihood plot with a cross at specified value
        plt.figure()
        plt.plot(par_rng, likelihoods, 'bo-')
        plt.plot(par_val, likelihoods[par_val-par_rng[0]], 'kx', markersize=24, markeredgewidth=2)
        plt.xlabel('Value Mapped')
        plt.ylabel('Log(Likelihood)')
        plt.title('Likelihood Function of Parameter %s: %s'
                  % (par_num, hammu12.jf12_parameter_names[par_num]))
        plt.minorticks_on()
        plt.savefig('movies/rm_plot_p%s_v%s.png' % (par_num, par_val))
        plt.close()

        # Import generated figures
        images = map(Image.open, ['movies/rm_map_p%s_v%s.png' % (par_num, par_val), 'movies/rm_plot_p%s_v%s.png' % (par_num, par_val)])

        # Correct for occasional incorrect transparancy in observable map
        images[0] = images[0].convert('RGBA')
        datas = images[0].getdata()
        newData = []
        for item in datas:
            if(item[3] == 0):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        images[0].putdata(newData)

        # Acquire size of both figures
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        # Combine both figures together and save it
        combined_image = Image.new('RGB', (total_width, max_height), color='#ffffff')
        x_offset = 0
        i = 0
        for image in images:
            y_offset = (max_height-heights[i])/2
            combined_image.paste(image, (x_offset, y_offset))
            x_offset += image.size[0]
            i += 1
        combined_image.save('movies/rm_com_p%s_v%s.png' % (par_num, par_val))
    else:
        raise ValueError("ERROR: Unknown observable profile")
