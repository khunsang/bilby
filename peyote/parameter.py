from __future__ import division, print_function, absolute_import
import numpy as np
from . import prior


class Parameter(object):

    def __init__(self, name, prior=None, latex_label=None):
        self.name = name

        self.prior = prior
        self.latex_label = latex_label

    @property
    def prior(self):
        return self.__prior

    @property
    def latex_label(self):
        return self.__latex_label

    @property
    def is_fixed(self):
        return isinstance(self.__prior, prior.DeltaFunction)

    @prior.setter
    def prior(self, prior=None):
        if prior is None:
            self.set_default_prior()
        else:
            self.__prior = prior

    @latex_label.setter
    def latex_label(self, latex_label=None):
        if latex_label is None:
            self.set_default_latex_label()
        else:
            self.__latex_label = latex_label

    def fix(self, value=None):
        """
        Specify parameter as fixed, this will not be sampled.
        """
        if value is None or np.isnan(value):
            raise ValueError("You can't fix the value to be np.nan. You need to assign it a legal value")
        self.prior = prior.DeltaFunction(value)

    def set_default_prior(self):

        if self.name == 'mass_1':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(5, 100))
        elif self.name == 'mass_2':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(5, 100))
        elif self.name == 'mchirp':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(5, 100))
        elif self.name == 'q':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 1))
        elif self.name == 'a1':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 1))
        elif self.name == 'a2':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 1))
        elif self.name == 'tilt1':
            self.__prior = prior.Sine()
        elif self.name == 'tilt2':
            self.__prior = prior.Sine()
        elif self.name == 'phi1':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 2 * np.pi))
        elif self.name == 'phi2':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 2 * np.pi))
        elif self.name == 'luminosity_distance':
            self.__prior = prior.PowerLaw(alpha=2, bounds=(1e2, 5e3))
        elif self.name == 'dec':
            self.__prior = prior.Cosine()
        elif self.name == 'ra':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 2 * np.pi))
        elif self.name == 'iota':
            self.__prior = prior.Sine()
        elif self.name == 'psi':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 2 * np.pi))
        elif self.name == 'phase':
            self.__prior = prior.PowerLaw(alpha=0, bounds=(0, 2 * np.pi))
        else:
            self.__prior = None

    def set_default_values(self):
        # spins
        if self.name == 'a1':
            self.__prior = prior.DeltaFunction(0)
        elif self.name == 'a2':
            self.__prior = prior.DeltaFunction(0)
        elif self.name == 'tilt1':
            self.__prior = prior.DeltaFunction(0)
        elif self.name == 'tilt2':
            self.__prior = prior.DeltaFunction(0)
        elif self.name == 'phi1':
            self.__prior = prior.DeltaFunction(0)
        elif self.name == 'phi2':
            self.__prior = prior.DeltaFunction(0)

    def set_default_latex_label(self):
        if self.name == 'mass_1':
            self.__latex_label = '$m_1$'
        elif self.name == 'mass_2':
            self.__latex_label = '$m_2$'
        elif self.name == 'mchirp':
            self.__latex_label = '$\mathcal{M}$'
        elif self.name == 'q':
            self.__latex_label = 'q'
        elif self.name == 'a1':
            self.__latex_label = 'a_1'
        elif self.name == 'a2':
            self.__latex_label = 'a_2'
        elif self.name == 'tilt1':
            self.__latex_label = 'tilt_1'
        elif self.name == 'tilt2':
            self.__latex_label = 'tilt_2'
        elif self.name == 'phi1':
            self.__latex_label = '\phi_1'
        elif self.name == 'phi2':
            self.__latex_label = '\phi_2'
        elif self.name == 'luminosity_distance':
            self.__latex_label = 'd_L'
        elif self.name == 'dec':
            self.__latex_label = '\mathrm{DEC}'
        elif self.name == 'ra':
            self.__latex_label = '\mathrm{RA}'
        elif self.name == 'iota':
            self.__latex_label = '\iota'
        elif self.name == 'psi':
            self.__latex_label = '\psi'
        elif self.name == 'phase':
            self.__latex_label = '\phi'
        elif self.name == 'tc':
            self.__latex_label = 't_c'
        else:
            self.__latex_label = self.name

    @staticmethod
    def parse_floats_to_parameters(old_parameters):
        parameters = old_parameters.copy()
        for key in parameters:
            if type(parameters[key]) is not float and type(parameters[key]) is not int \
                    and type(parameters[key]) is not Parameter:
                print("Expected parameter " + str(key) + " to be a float or int but was " + str(type(parameters[key]))
                      + " instead. Will not be converted.")
                continue
            elif type(parameters[key]) is Parameter:
                continue

            parameters[key] = Parameter(key)
            parameters[key].fix(old_parameters[key])
        return parameters

    @staticmethod
    def parse_keys_to_parameters(keys):
        parameters = {}
        for key in keys:
            parameters[key] = Parameter(key)
        return parameters