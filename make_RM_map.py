from imagine import *
from nifty import *
import numpy as np
import sys

parameters = [0]*30
hammu12 = Hammurapy_jf12(350, 350, random_disk_field_falloff='1/r',
                         hammurabi_path='/home/gvelden/imagine_downloads/hammurabi_3')

# Acquire some important Hammurabi parameters
obs_shell_index_numb = int(hammu12.get_default_parameters_dict()['obs_shell_index_numb'])
total_shell_numb = int(hammu12.get_default_parameters_dict()['total_shell_numb'])
obs_NSIDE = int(hammu12.get_default_parameters_dict()['obs_NSIDE'])
vec_size_R = int(hammu12.get_default_parameters_dict()['vec_size_R'])
max_radius = int(hammu12.get_default_parameters_dict()['max_radius'])
data_file = str(hammu12.get_default_parameters_dict()['TE_grid_filename'])

# Set the boundary of the observable map. Set to None for no boundaries.
boundary = 100
h = hp_space(obs_NSIDE)

obs = hammu12.calc_observables(parameters)

# Generate and save the observable map
field(h, val=obs['rm_observable']['rm_map']).plot(save='rm_map (%s, %s, %s, %s, %s, %s, %s).png' % (obs_shell_index_numb, total_shell_numb, obs_NSIDE, vec_size_R, max_radius, boundary, data_file), title='RM Map: %s, %s, %s, %s, %s, %s, %s' % (obs_shell_index_numb, total_shell_numb, obs_NSIDE, vec_size_R, max_radius, boundary, data_file), unit='Rotation Measure $[\mathrm{rad/m^2}]$', vmin=-1*boundary, vmax=boundary)

# Save the raw-data of observable map in a .npy-file
np.save('rm_map (%s, %s, %s, %s, %s, %s, %s)' % (obs_shell_index_numb, total_shell_numb, obs_NSIDE, vec_size_R, max_radius, boundary, data_file), obs['rm_observable']['rm_map'])

# Save the currently used Hammurabi parameters in a .txt-file
sys.stdout=open('rm_map (%s, %s, %s, %s, %s, %s, %s).txt' % (obs_shell_index_numb, total_shell_numb, obs_NSIDE, vec_size_R, max_radius, boundary, data_file), 'w')
print(hammu12.last_call_log)
sys.stdout.close()
