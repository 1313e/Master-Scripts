from imagine import *
from nifty import *
import numpy as np

hammu12 = Hammurapy_jf12(350, 350,
                         hammurabi_path='/home/gvelden/imagine_downloads/hammurabi_3')

parameters = [0]*hammu12.get_parameter_dimension()

obs = hammu12.calc_observables(parameters)

# np.save('sync_I', obs['sync_observable']['sync_I'])
# np.save('sync_Q', obs['sync_observable']['sync_Q'])
# np.save('sync_U', obs['sync_observable']['sync_U'])
np.save('rm_map', obs['rm_observable']['rm_map'])
# np.save('dm_map', obs['dm_observable']['dm_map'])
# np.save('dust_I', obs['dust_observable']['dust_I'])
# np.save('dust_Q', obs['dust_observable']['dust_Q'])
# np.save('dust_U', obs['dust_observable']['dust_U'])
# np.save('tau_map', obs['tau_observable']['tau_map'])
# np.save('ff_map', obs['ff_observable']['ff_map'])
