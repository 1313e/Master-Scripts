from imagine import *
from nifty import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

hammu12 = Hammurapy_jf12(350, 350, random_disk_field_falloff='1/r',
                         hammurabi_path='/home/gvelden/imagine_downloads/'
                                        'hammurabi_3')
likelihood = Meta_likelihood([RM_likelihood()])

# If called, make file containing current Hammurabi parameters if not present
if not os.path.exists('last_call_log.txt'):
    parameters = [0]*30
    obs = hammu12.calc_observables(parameters)

    stdout = sys.stdout
    sys.stdout = open('last_call_log.txt', 'w')
    print(hammu12.last_call_log)
    sys.stdout = stdout


# Set prior to unity
class trivial_prior_class(prior_calculator):
    def calc_prior(self, parameter):
        return 1.


# Calculates likelihood for given parameter number and range
def calc_likelihood(par_num, par_rng):
    """
    Calculates the likelihood of a given parameter with parameter number
    `par_num` in carrier mapper-range `par_rng`.

    Parameters
    ----------
    par_num : int
        Number of parameter corresponding to the index of parameter in
        Hammurabi.
    par_rng : :mod:`~numpy.ndarray`
        Range of carrier mapper values for which the likelihood needs to be
        calculated.

    Returns
    -------
    out : .npy-file
        .npy-file containing the likelihood of given parameter and range

    """

    likelihoods = np.zeros(np.size(par_rng))

    trivial_prior = trivial_prior_class()

    pipe = pipeline(observables_generator=hammu12,
                    likelihood=likelihood,
                    prior=trivial_prior,
                    optimizer_class=Hamiltonian_Monte_Carlo)

    parameters = [0]*hammu12.get_parameter_dimension()
    for par_val in par_rng:
        parameters[par_num] = par_val
        likelihoods[par_val-par_rng[0]] = pipe._calc_posterior(parameters)

    np.save('data%s_RM' % (par_num), likelihoods)


# Plots likelihood for given parameter number and range
def plot_likelihood(par_num, par_rng):
    """
    Plots the likelihood of a given parameter with parameter number
    `par_num` in carrier mapper-range `par_rng`.

    Parameters
    ----------
    par_num : int
        Number of parameter corresponding to the index of parameter in
        Hammurabi.
    par_rng : :mod:`~numpy.ndarray`
        Range of carrier mapper values for which the likelihood needs to be
        plotted.

    Returns
    -------
    out : .png-file
        .png-file containing the plot of the likelihood of given parameter and
        range

    """

    likelihoods = np.load('data%s_RM.npy' % (par_num))

    plt.figure()
    plt.plot(par_rng, likelihoods, 'bo-')
    plt.xlabel('Value Mapped')
    plt.ylabel('Log(Likelihood)')
    plt.title('Likelihood Function of Parameter %s: %s'
              % (par_num, hammu12.jf12_parameter_names[par_num]))
    plt.minorticks_on()
    plt.savefig('fig%s_RM.png' % (par_num))
    plt.close()
