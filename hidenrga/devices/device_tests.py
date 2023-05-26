import device

import unittest


class TestHidenRGASimulator(unittest.TestCase):

    def setUp(self):
        self._simulator = device.SimulatedHidenRGA()
        self._simulator.current_gas = "H2"
        self._simulator.current_gas_pressure = 1E-7
        self._simulator.current_gas = "D2"
        self._simulator.current_gas_pressure = 2E-7
        self._simulator.current_gas = "He"
        self._simulator.current_gas_pressure = 3E-7
        self._simulator.current_gas = "H2O"
        self._simulator.current_gas_pressure = 4E-7
        self._simulator.current_gas = "CO"
        self._simulator.current_gas_pressure = 5E-7
        self._simulator.dwell = 0

    def Ascan(self):
        self._simulator.start("Ascans")
        data = self._simulator.data(True)
        self._simulator.stop(StopOptions.StopOptions.SCAN)
        while True:
            new_data = self._simulator.data(False)
            if new_data == "*C110*":
                break
            data += new_data
        # Format data so it's readable.
        data = data.replace(",}]", "\n}]")
        data = data.replace(",", ",\n  ")
        data = data.replace("][", "]\n[")
        print(data)
        self.assertTrue(self._simulator.data_queue.empty())
        self.assertTrue(self._simulator.data() == "*C110*")
        
    def test_contiguous_mass(self):
        print("")
        print("test_contiguous_mass")
        self._simulator.electron_energy = 70
        self._simulator.noise = 0
        self._simulator.cycles = 2
        self._simulator.current_scan = "Ascans"
        self._simulator.report = 21
        self._simulator.scan_output = "mass"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 1.0
        self._simulator.current_row_start = 1
        self._simulator.current_row_stop = 30
        self.Ascan()
        
    def test_non_contiguous_mass(self):
        print("")
        print("test_non_contiguous_mass")
        self._simulator.noise = 0
        self._simulator.electron_energy = 70
        self._simulator.cycles = 1
        self._simulator.current_scan = "Ascans"
        self._simulator.report = 5
        self._simulator.scan_output = "mass"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 0.2
        self._simulator.current_row_start = 1
        self._simulator.current_row_stop = 3
        self._simulator.current_row = 1
        self._simulator.current_row_step = 0.2
        self._simulator.current_row_start = 17
        self._simulator.current_row_stop = 19
        self._simulator.current_row = 2
        self._simulator.current_row_step = 0.2
        self._simulator.current_row_start = 27
        self._simulator.current_row_stop = 29
        self.Ascan()
    
    def test_contiguous_energy(self):
        print("")
        print("test_contiguous_energy")
        self._simulator.noise = 0
        self._simulator.mass = 4
        self._simulator.cycles = 1
        self._simulator.current_scan = "Ascans"
        self._simulator.report = 5
        self._simulator.scan_output = "energy"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 1
        self._simulator.current_row_start = 10
        self._simulator.current_row_stop = 40
        self.Ascan()

    def test_non_contiguous_energy(self):
        print("")
        print("test_non_contiguous_energy")
        self._simulator.noise = 0
        self._simulator.mass = 4
        self._simulator.cycles = 1
        self._simulator.current_scan = "Ascans"
        self._simulator.report = 5
        self._simulator.scan_output = "energy"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 1
        self._simulator.current_row_start = 15
        self._simulator.current_row_stop = 20
        self._simulator.current_row = 1
        self._simulator.current_row_step = 1
        self._simulator.current_row_start = 30
        self._simulator.current_row_stop = 40
        self.Ascan()

    def test_contiguous_mass_and_energy(self):
        print("")
        print("test_contiguous_mass_and_energy")
        self._simulator.noise = 0
        self._simulator.cycles = 1
        self._simulator.current_scan = "Ascans"
        self._simulator.report = 0
        self._simulator.scan_output = "energy"
        self._simulator.scan_input = "Bscans"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 5
        self._simulator.current_row_start = 20
        self._simulator.current_row_stop = 60
        self._simulator.current_scan = "Bscans"
        self._simulator.report = 5
        self._simulator.scan_output = "mass"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 1
        self._simulator.current_row_start = 10
        self._simulator.current_row_stop = 50
        self._simulator.current_scan = "Ascans"
        self.Ascan()
        
    def test_non_contiguous_mass_and_energy(self):
        print("")
        print("test_non_contiguous_mass_and_energy")
        self._simulator.noise = 0
        self._simulator.cycles = 1
        self._simulator.current_scan = "Ascans"
        self._simulator.report = 0
        self._simulator.scan_output = "energy"
        self._simulator.scan_input = "Bscans"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 1
        self._simulator.current_row_start = 15
        self._simulator.current_row_stop = 25
        self._simulator.current_row = 1
        self._simulator.current_row_step = 1
        self._simulator.current_row_start = 35
        self._simulator.current_row_stop = 45
        self._simulator.current_scan = "Bscans"
        self._simulator.report = 5
        self._simulator.scan_output = "mass"
        self._simulator.current_row = 0
        self._simulator.current_row_step = 0.2
        self._simulator.current_row_start = 3
        self._simulator.current_row_stop = 5
        self._simulator.current_row = 1
        self._simulator.current_row_step = 0.2
        self._simulator.current_row_start = 27
        self._simulator.current_row_stop = 29
        self._simulator.current_scan = "Ascans"
        self.Ascan()


if __name__ == '__main__':
    unittest.main()
