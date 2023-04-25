##################################################
#
# Device simulator File
#
# Simulator file for Hiden RGA
# ITER, April 2023
# Author : P.J. L. Heesterman (Capgemini Engineering)
#
# NOTES:
#
# 
#
##################################################
from collections import OrderedDict
from lewis.core.logging import has_log
from lewis.core.statemachine import State
from lewis.devices import StateMachineDevice
from numpy.random import normal
import time
import threading
import queue
import math
import sys

try:
    from . import gasses  # "emulator" case
except ImportError:
    import gasses  # "__main__" case


class DefaultState(State):
    """
    Device is in default state.
    """
    NAME = 'Default'


class ScanThread(threading.Thread):
    def __init__(self, device, name):
        super().__init__()
        self._device = device
        self.name = name

    def run(self):
        cycle = 0
        self._device._stopping = False
        while self._device.cycles == 0 or cycle < self._device.cycles:
            if self._device._stopping:
                break
            self._device.scan()
            if self._device.cycles != 0:
                cycle += 1


class ScannerRow:
    def __init__(self):
        self._start = 0
        self._stop = 0
        self._step = 1
        
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def stop(self):
        return self._stop
        
    @stop.setter
    def stop(self, stop):
        self._stop = stop

    @property
    def step(self):
        return self._step
        
    @step.setter
    def step(self, step):
        self._step = step


class Scanner:
    def __init__(self):
        self._rows = [ScannerRow()]
        self._current_row = 0
        self._scan_input = "Faraday"
        self._scan_output = "mass"
        
    @property
    def rows(self):
        return self._rows
        
    @property
    def current_row(self):
        return self._current_row
        
    @current_row.setter
    def current_row(self, current_row):
        if len(self._rows) <= current_row:
            self._rows.insert(current_row, ScannerRow())
        self._current_row = current_row
        
    @property
    def start(self):
        return self._rows[self.current_row].start
        
    @start.setter
    def start(self, start):
        self._rows[self.current_row].start = start
        
    @property
    def stop(self):
        return self._rows[self.current_row].stop
        
    @stop.setter
    def stop(self, stop):
        self._rows[self.current_row].stop = stop
        
    @property
    def step(self):
        return self._rows[self.current_row].step
        
    @step.setter
    def step(self, step):
        self._rows[self.current_row].step = step

    @property
    def scan_input(self):
        return self._scan_input
            
    @scan_input.setter
    def scan_input(self, input):
        self._scan_input = input

    @property
    def scan_output(self):
        return self._scan_ouput
            
    @scan_output.setter
    def scan_output(self, output):
        self._scan_output = output

        
class SimulatedHidenRGA(StateMachineDevice):
    def __init__(self):
        super().__init__()
        self._scan_thread = None
        self._current_scan = None
        self._gasses = gasses.Gasses()
        self._current_gas = None
        self._initialize_data()

    def _initialize_data(self):
        self.connected = True
        self._name = "HAL RC RGA 201 #13656"
        self._scans = {}
        self._terse = False
        self._min_mass = 0
        self._max_mass = 100
        self._electron_energy = 70
        self._emission = 100
        self._stopping = False
        self._cycles = 0
        self._interval = 0
        self._data_queue = queue.Queue()
        self._points = 70
        self._emok = True
        self._filok = True
        self._ptrip = False
        self._overtemp = False
        self._zero = False
        self._mode = 1
        self._report = 5
        self._dwell = 100
        self._dwellmode = True
        self._settle = 100
        self._settlemode = True
        self._noise = 1E-9
        self._total_pressure = 0
        self._terse = True

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()

    @property
    def name(self):
        return self._name

    @property
    def terse(self):
        return self._terse

    @terse.setter
    def terse(self, terse):
        self._terse = terse
        
    @property
    def data_queue(self):
        return self._data_queue

    def data(self, all=False):
        fields_in_report = 0;
        if (self.report & 16) != 0:  # Bit 4, elapsed time in ms
            fields_in_report += 1
        if (self.report & 4) != 0:   # Bit 2, output value
            fields_in_report += 1
        if (self.report & 1) != 0:   # Bit 0, return input value
            fields_in_report += 1
    
        if self._data_queue.empty():
            if not self.stat:
                return "*C110*"     # No more data available
            else:
                return ""
        qsize = round(math.ceil(self._data_queue.qsize() / fields_in_report))
        return_size = qsize
        points = self.points * fields_in_report
        if not all and return_size < points:
            return_size = points
        point = 0
        return_string = ""
        while point < return_size:
            if self._stopping:
                break
            if self._data_queue.empty():
                break
            if (self.report & 4) != 0:
                scan_point = self._data_queue.get()
                if scan_point == self.current_scan.start:
                    return_string += "{"
                return_string += str(scan_point)
                self._data_queue.task_done()
                return_string += ":"
            if (self.report & 1) != 0:
                value = self._data_queue.get()
                if value >= 0:
                    return_string += " "
                return_string += str(value)
                self._data_queue.task_done()
                return_string += ","
            if (self.report & 4) != 0:
                if scan_point >= self.current_scan.stop:
                    return_string += "}"
                    if not self.stat:
                        return_string += "!"
                    break
            point += 1
        self.log.info("Data returned " + return_string)
        return return_string

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def emok(self):
        return self._emok

    @property
    def filok(self):
        return self._filok

    @property
    def ptrip(self):
        return self._ptrip

    @property
    def overtemp(self):
        return self._overtemp

    @property
    def current_scan(self):
        return self._current_scan

    @current_scan.setter
    def current_scan(self, current_scan):
        if current_scan not in self._scans:
            self._scans[current_scan] = Scanner()
        self._current_scan = self._scans[current_scan]

    @property
    def current_row(self):
        return self._current_scan.current_row
        
    @current_row.setter
    def current_row(self, current_row):
        self._current_scan.current_row = current_row

    @property
    def rows(self):
        return self._current_scan.rows
        
    @property
    def scan_output(self):
        return self_current_scan.scan_output

    @scan_output.setter
    def scan_output(self, output):
        self._current_scan.scan_output = output

    @property
    def scan_input(self):
        return self._current_scan.scan_input

    @scan_input.setter
    def scan_input(self, input):
        self._current_scan.scan_input = input

    @property
    def min_mass(self):
        return self._min_mass

    @property
    def scan_start(self):
        return self._current_scan.start

    @scan_start.setter
    def scan_start(self, start):
        self._current_scan.start = start

    @property
    def max_mass(self):
        return self._max_mass

    @property
    def scan_stop(self):
        return self._current_scan.stop

    @scan_stop.setter
    def scan_stop(self, stop):
        self._current_scan.stop = stop

    @property
    def scan_step(self):
        return self._current_scan.step

    @scan_step.setter
    def scan_step(self, step):
        self._current_scan.step = step

    @property
    def cycles(self):
        return self._cycles

    @cycles.setter
    def cycles(self, cycles):
        self._cycles = cycles

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        self._interval = interval

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, low):
        self._low = low

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, high):
        self._high = high

    @property
    def zero(self):
        return self._zero

    @zero.setter
    def zero(self, zero):
        self._zero = zero

    @property
    def electron_energy(self):
        return self._electron_energy
        
    @electron_energy.setter
    def electron_energy(self, electron_energy):
        self._electron_energy = electron_energy
        
    @property
    def emission(self):
        return self._emission
        
    @emission.setter
    def emission(self, emission):
        self._emission = emission
        
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, report):
        self._report = report

    @property
    def dwell(self):
        return self._dwell

    @dwell.setter
    def dwell(self, dwell):
        self._dwell = dwell

    @property
    def dwellmode(self):
        return self._dwellmode

    @dwellmode.setter
    def dwellmode(self, dwellmode):
        self._dwellmode = dwellmode

    @property
    def settle(self):
        return self._settle

    @settle.setter
    def settle(self, settle):
        self._settle = settle

    @property
    def settlemode(self):
        return self._settlemode

    @settlemode.setter
    def settlemode(self, settlemode):
        self._settlemode = settlemode

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, noise):
        self._noise = noise

    @property
    def current_gas(self):
        return self._current_gas

    @current_gas.setter
    def current_gas(self, name):
        if self._gasses.gas(name) is None:
            self.log.error("Unknown gas " + name)
            return
        self._current_gas = name

    @property
    def current_gas_pressure(self):
        if self._current_gas is None:
            self.log.error("No gas selected.")
            return
        return self._gasses.gas(self._current_gas).partial_pressure

    @current_gas_pressure.setter
    def current_gas_pressure(self, partial_pressure):
        if self._current_gas is None:
            self.log.error("No gas selected.")
            return
        self._total_pressure += partial_pressure - self.current_gas_pressure
        if self._total_pressure > 1E-4:
            self._ptrip = True
            self._emission = 0
            self._scan_input = "Faraday"
        self._gasses.gas(self._current_gas).partial_pressure = partial_pressure
        
    @property
    def total_pressure(self):
        return self._total_pressure

    def start(self):
        self._scan_thread = ScanThread(self, "scan_thread")
        while not self._data_queue.empty():
            self._data_queue.get()
            self._data_queue.task_done()
        self._scan_thread.start()

    @property
    def stat(self):
        if self._scan_thread is None:
            return False
        return self._scan_thread.is_alive()

    def stop(self, stopping=True):
        """Stops scanning immediately """
        self.log.info("Stop scanning now.")
        self._stopping = stopping
        if self._scan_thread is not None:
            self._scan_thread.join()
        self._scan_thread = None

    def scan_row(self, start_time):
        data_point = 0
        data_points = round((self.scan_stop - self.scan_start) / self.scan_step)
        while data_point <= data_points:
            if self._stopping:
                break
            scan_point = self.scan_start + self.scan_step * data_point
            time.sleep(self._dwell / 1000.0)
            noise = normal(-self._noise, self._noise)
            if self._current_scan.scan_input == "SEM":
                # Lower noise in SEM mode.
                noise /= 1000
            signal = self._gasses.signal(scan_point, self._electron_energy)
            if (self.report & 16) != 0: # Bit 4, elapsed time in ms
                self._data_queue.put((time.monotonic - start_time) * 1000)
            if (self.report & 4) != 0:  # Bit 2, output value
                self._data_queue.put(scan_point)
            if (self.report & 1) != 0:  # Bit 0, return input value
                self._data_queue.put(signal + noise)
            data_point += 1
            
    def scan(self):
        start_time = time.monotonic
        for self.current_row, item in enumerate(self._current_scan.rows):
            self.scan_row(start_time)


if __name__ == '__main__':
    """ For debug purpose only. """
    Simulator = SimulatedHidenRGA()
    Simulator.current_gas = "H2"
    Simulator.current_gas_pressure = 1E-7
    Simulator.current_gas = "H2O"
    Simulator.current_gas_pressure = 2E-7
    Simulator.current_gas = "CO"
    Simulator.current_gas_pressure = 3E-7
    Simulator.noise = 0
    Simulator.cycles = 1
    Simulator.current_scan = "Ascans"
    Simulator.current_row = 0
    Simulator.scan_step = 0.2
    Simulator.scan_start = 1
    Simulator.scan_stop = 3
    Simulator.current_row = 1
    Simulator.scan_step = 0.2
    Simulator.scan_start = 17
    Simulator.scan_stop = 19
    Simulator.current_row = 2
    Simulator.scan_step = 0.2
    Simulator.scan_start = 27
    Simulator.scan_stop = 29
    Simulator.start()
    Simulator.stop(False)
    print(Simulator.data(False))
    assert(Simulator.data_queue.empty())
    assert(Simulator.data() == "*C110*")
