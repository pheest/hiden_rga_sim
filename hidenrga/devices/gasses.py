import numpy as np
import pprint

import logging
logging.basicConfig(level=logging.INFO, filename='gasses.log', format='%(asctime)s [%(levelname)5s] %(name)s: %(message)s', filemode="w")
LOG = logging.getLogger(__name__)

class GasSpecies:

    def __init__(self, name, ionisation_energy):
        self._name = name
        self._mass = 0
        self._ionisation_energy = ionisation_energy
        self._partial_pressure = 0

    @property
    def name(self):
        return self._name

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        self._mass = mass

    @property
    def ionisation_energy(self):
        return self._ionisation_energy

    @property
    def partial_pressure(self):
        return self._partial_pressure

    @partial_pressure.setter
    def partial_pressure(self, partial_pressure):
        self._partial_pressure = partial_pressure

    def ionisation_efficiency(self, electron_energy):
        """ This curve is probably about right """
        # https://pubs.aip.org/aip/jcp/article/154/11/114104/315339/The-efficient-calculation-of-electron-impact
        if electron_energy < self._ionisation_energy:
            return 0
        over_threshold = electron_energy - self._ionisation_energy

        return 3 * over_threshold / pow(electron_energy, 1.2)

    def signal(self, mass, electron_energy):
        if self._partial_pressure == 0:
            return 0
        sigma = 0.25  # Clear between peaks to ~12%
        gaussian = np.exp(-np.power((mass - self._mass)/sigma, 2.)/2.)
        
        signal = self._partial_pressure * self.ionisation_efficiency(electron_energy) * gaussian
        return signal


class Gasses:

    def __init__(self):
        self._masses = []         # List of masses
        self._masses_map = {}     # Dict of mass index to species name
        self._species = {}        # Dict of species name to species
        # https://en.wikipedia.org/wiki/Ionization_energies_of_the_elements_(data_page)
        self.insert(1, GasSpecies("H", 13.59844))
        self.insert(4, GasSpecies("He", 24.58738))
        self.insert(14, GasSpecies("N", 14.53414))
        self.insert(16, GasSpecies("O", 13.61806))
        self.insert(19, GasSpecies("F", 17.42282))
        self.insert(40, GasSpecies("A", 15.75962))

        self.insert(2, GasSpecies("H2", 15.425927)) # https://webbook.nist.gov/cgi/cbook.cgi?ID=C1333740&Mask=20
        self.insert(4, GasSpecies("D2", 15.46658))  # https://webbook.nist.gov/cgi/cbook.cgi?ID=C7782390&Mask=20
        self.insert(18, GasSpecies("H2O", 12.6223)) # https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=20
        self.insert(28, GasSpecies("N2", 15.581))   # https://webbook.nist.gov/cgi/cbook.cgi?ID=C7727379&Mask=20
        self.insert(28, GasSpecies("CO", 14.0142))  # https://webbook.nist.gov/cgi/cbook.cgi?ID=C630080&Mask=20
        self.insert(32, GasSpecies("O2", 12.0697))  # https://webbook.nist.gov/cgi/cbook.cgi?ID=C7782447&Mask=20
        self.insert(38, GasSpecies("F2", 15.697))   # https://webbook.nist.gov/cgi/inchi?ID=C7782414&Mask=20
        self.insert(44, GasSpecies("CO2", 13.778))  # https://webbook.nist.gov/cgi/cbook.cgi?ID=C124389&Mask=20

    def insert(self, mass, gas_species):
        index = np.searchsorted(self._masses, mass, side='right')
        self._masses.insert(index, mass)
        if index in self._masses_map:
            for key in range(len(self._masses_map), index, -1):
                self._masses_map[key] = self._masses_map[key-1]
        self._masses_map[index] = gas_species.name
        gas_species.mass = mass
        self._species[gas_species.name] = gas_species

    @property
    def species(self):
        return self._species

    @property
    def masses_map(self):
        return self._masses_map

    def gas(self, name):
        if name not in self.species:
            return None
        return self._species[name]

    def signal(self, mass, electron_energy):
        total_signal = 0
        width = 0.75
        index_left = np.searchsorted(self._masses, mass-width, side='left')
        index_right = np.searchsorted(self._masses, mass+width, side='right')
        # [1, 2, 4, 4, 14, 16, 18, 18, 19, 28, 28, 32, 38, 44]
        if index_right >= len(self._masses_map):
            index_right = len(self._masses_map)-1
            
        index = index_left
        while index <= index_right:
            species_name = self._masses_map[index]
            species = self._species[species_name]
            if abs(species.mass-mass) < width and species.partial_pressure != 0:
                signal_value = species.signal(mass, electron_energy)
                LOG.debug("Species " + species.name + " species mass " + str(species.mass) + " mass " + str(mass) + " electron energy " + str(electron_energy) + " signal " + str(signal_value))
                total_signal += signal_value
            index += 1
        return total_signal

    @property
    def masses(self):
        return self._masses


if __name__ == "__main__":
    """ For debugging purpose only """
    gasses = Gasses()
    pprint.pprint(gasses.masses_map)
    for name in gasses.species:
        species = gasses.species[name]
        print(name, species.mass, species.ionisation_energy, species.ionisation_efficiency(70))
    pprint.pprint(gasses.masses)

    H2 = gasses.gas("H2")
    H2.partial_pressure = 1E-5  # NB, Pascal units

    He = gasses.gas("He")
    He.partial_pressure = 1E-5  # NB, Pascal units

    D2 = gasses.gas("D2")
    D2.partial_pressure = 1E-5  # NB, Pascal units

    H2O = gasses.gas("H2O")
    H2O.partial_pressure = 2E-5  # NB, Pascal units
    
    CO = gasses.gas("CO")
    CO.partial_pressure = 1E-6  # NB, Pascal units

    CO2 = gasses.gas("CO2")
    CO.partial_pressure = 2E-6  # NB, Pascal units

    N2 = gasses.gas("N2")
    N2.partial_pressure = 8E-5  # NB, Pascal units

    O2 = gasses.gas("O2")
    O2.partial_pressure = 2E-5  # NB, Pascal units

    for mass in np.arange(17.25, 18.76, 0.01):
        print("mass " + str(mass) + " signal " + str(gasses.signal(mass, 70)))

    for ee in range(15, 40):
        print("energy " + str(ee) + " D2 signal " + str(D2.signal(D2.mass, ee)) + " He signal " + str(He.signal(He.mass, ee)))
