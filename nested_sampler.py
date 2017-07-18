# -*- coding: utf-8 -*-
"""
Imagine Pipeline

Ellert van der Velden (ellert.vandervelden@student.ru.nl) 2016
"""
import logging
import numpy as np
from numpy.random import uniform,\
                         choice,\
                         normal

from imagine.base_classes import optimizer

logger = logging.getLogger('NESTED')


class Nested_sampler(optimizer):
    def __init__(self, dimension, f, fprime=None):
        super(Nested_sampler, self).__init__(dimension, f, fprime)

        self.dimension = dimension # Dimension
        self.number_of_samples = max(3*self.dimension, 10) # Number of samples used in the sampler
        self.chain = [np.zeros(self.dimension)] # No use right now

        self.f = f # Likelihood function
        self.fprime = fprime # Derivative of likelihood function (unused, since nested does not need it)

        self.number_of_sampler_steps = 100*self.number_of_samples # Number of optimization steps
        self.number_of_MCMC_steps = 20 # Minimum number of random-walk steps per optimization step
        self.max_number_of_MCMC_steps = 20 # Maximum number of random-walk steps in an optimization step
        self.max_number_of_failures = 0 # Maximum number of times an optimization step is allowed to fail

        self._initialize_procedure() # Start sampling

    def _initialize_procedure(self):
        Z = 0 # Evidence
        fc = 0 # Optimization failures count
        f_args = [] # List containing all non-valid indices for being a starting likelihood
        X = np.zeros(self.number_of_sampler_steps+1) # Prior mass
        X[0] = 1 # Initial prior mass
        L = np.zeros(self.number_of_samples) # Likelihoods
        Li = 0 # Lowest likelihood
        step_size = 1 # Random-walk stepsize
        # k = [8, 10, 14] # Parameters that needs to be changed for testing purposes
        k = np.linspace(0, self.dimension-1, self.dimension) # Pick all parameters

        parameters = np.zeros([self.number_of_samples, self.dimension])

        for i in xrange(self.number_of_samples): # Obtain random parameter samples
            for n in k:
                parameters[i, n] = uniform(-100, 100)
            L[i] = self.f(parameters[i])
        # print(parameters)
        # print(L)

        for i in xrange(self.number_of_sampler_steps):
            arg_min = np.argmin(L) # Find the worst likelihood
            f_args += [arg_min]
            np.sort(f_args)
            # print(arg_min)
            Li = L[arg_min] # Save that likelihood
            parameters_i = parameters[arg_min]
            # print(Li)
            X[i+1] = np.exp(-(i+1)/self.number_of_samples) # Update the prior mass
            wi = X[(i+1)-1]-X[(i+1)] # Weight
            Z += wi*Li # Update the evidence

            # Start: Find a better likelihood (MH)
            arg_list = range(0, f_args[0]) # Make the list containing only indices of likelihoods that are allowed to start at
            for l in xrange(np.size(f_args)-1):
                arg_list += range(f_args[l]+1, f_args[l+1])
            arg_list += range(f_args[-1]+1, self.number_of_samples)
            # arg_new = choice(range(0, arg_min) + range(arg_min+1, self.number_of_samples)) # Replace Li (L[arg_min]) by a random L
            arg_new = choice(arg_list)
            L[arg_min] = L[arg_new]
            parameters[arg_min] = parameters[arg_new]

            accept = 0
            reject = 0
            j = 0
            jn = self.number_of_MCMC_steps
            while(j < jn):
                j += 1
                parameters_try = np.zeros(self.dimension)
                for n in k:
                    parameters_try[n] = parameters[arg_min, n] + step_size*normal(0, 1)
                L_try = self.f(parameters_try)
                if(L_try > Li): # If L_try is better than Li, replace L[arg_min] by L_try
                    parameters[arg_min] = parameters_try
                    L[arg_min] = L_try
                    accept += 1
                    fc = 0
                    f_args = []
                else: # If L_try is worse than Li, do not replace anything
                    reject += 1
                if(accept > reject): # If more get accepted than rejected, increase the random-walk stepsize
                    step_size *= np.exp(1/accept)
                elif(accept < reject): # If more get rejected than accepted, decrease the random-walk stepsize
                    step_size /= np.exp(1/reject)
                if(j == jn and accept == 0 and jn < self.max_number_of_MCMC_steps): # If none have been accepted and there have not been max_number_of_MCMC_steps yet, do 5 more steps.
                    jn += 5
                    print(jn)
                elif(j == jn and accept == 0 and jn == self.max_number_of_MCMC_steps and fc < self.max_number_of_failures): # If max_number_of_MCMC_steps have passed and none have been accepted, the best likelihood has already been found, thus breaking the outer for-loop.
                    fc += 1
                    print(fc)
                    L[arg_min] = Li
                    parameters[arg_min] = parameters_i
                    f_args += [arg_new]
                    np.sort(f_args)
                    i -= 1
                elif(j == jn and accept == 0 and jn == self.max_number_of_MCMC_steps and fc == self.max_number_of_failures):
                    break
            else:
                continue
            break
            # End
        Z += (np.sum(L)*X[self.number_of_sampler_steps])/self.number_of_samples # Update evidence with the latest calculation
        # print(L)
        print(i)
        self.parameters = parameters[np.argmax(L)] # Obtain best parameter set
        self.L = L[np.argmax(L)] # Obtain best likelihood
        self.Z = Z # Obtain evidence
        self.P = self.L/self.Z # Obtain posterior
