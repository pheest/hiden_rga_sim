import numpy as np
import pprint


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
        return self._partial_pressure * self.ionisation_efficiency(electron_energy) * gaussian


class Gasses:

    def __init__(self):
        self._masses = []
        self._species = []
        self._map = {}
        # https://en.wikipedia.org/wiki/Ionization_energies_of_the_elements_(data_page)
        self.insert(1, GasSpecies("H", 13.59844))
        self.insert(4, GasSpecies("He", 24.58738))
        self.insert(14, GasSpecies("N", 14.53414))
        self.insert(16, GasSpecies("O", 13.61806))
        self.insert(18, GasSpecies("A", 15.75962))
        self.insert(19, GasSpecies("F", 17.42282))

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
        gas_species.mass = mass
        self._species.insert(index, gas_species)
        self._map[gas_species.name] = index

    @property
    def species(self):
        return self._species

    @property
    def map(self):
        return self._map

    def gas(self, name):
        if name not in self._map:
            return None
        index = self._map[name]
        return self._species[index]

    def signal(self, mass, electron_energy):
        signal_value = 0
        index_left = np.searchsorted(self._masses, mass, side='left')
        if index_left >= len(self._species):
            index_left -= 1
        while index_left > 0 and self._species[index_left].mass >= mass-1:
            index_left -= 1
        index_right = np.searchsorted(self._masses, mass, side='right')
        if index_right >= len(self._species):
            index_right -= 1
        while index_right < len(self._species)-1 and self._species[index_right].mass <= mass+1:
            index_right += 1
        index = index_left
        while index <= index_right:
            signal_value += self._species[index].signal(mass, electron_energy)
            index += 1
        return signal_value

    @property
    def masses(self):
        return self._masses


if __name__ == "__main__":
    """ For debugging purpose only """
    gasses = Gasses()
    pprint.pprint(gasses.map)
    for species in gasses.species:
        print(species.name, species.ionisation_energy, species.ionisation_efficiency(1070))
    pprint.pprint(gasses.masses)
