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
import math
import sys

try:
    from . import gasses  # "emulator" case
except ImportError:
    import gasses  # "__main__" case
    
try:
    from . import scanner  # "emulator" case
except ImportError:
    import scanner  # "__main__" case
    
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
        """ 
        Thread method to aquire data
        """
        cycle = 0
        self._device._stopping = False
        # Cache these values as they will be overwritten
        mass = self._device.mass
        electron_energy = self._device.electron_energy
        start_time = time.monotonic()
        while self._device.cycles == 0 or cycle < self._device.cycles:
            if self._device._stopping:
                break
            self._device.scan(start_time)
            if self._device.cycles != 0:
                cycle += 1
        # Restore these values
        self._device.mass = mass
        self._device.electron_energy = electron_energy


class SimulatedHidenRGA(StateMachineDevice):
    def __init__(self):
        super().__init__()
        self._scan_thread = None
        self._gasses = gasses.Gasses()
        self._current_gas = None
        self._name = "HAL RC RGA 101X #17995"
        self._release = "Release 3.2, 26/4/23"
        self._scan_table = ["scan","row","cycles","interval","state","output","start","stop","step","input","rangedev","low", \
                            "high","current","zero","dwell","settle","mode","report","options","return","type","env"]
        self._logical_groups = ["rangedev","total/partial","switched","measurement","quad","degassing","mode","all","map","input", \
                                "output","environment","others","global","control"]
        self._logical_rangedev = ["Faraday_range","Total_range","auxiliary1_range","auxiliary2_range","nul_range"]
        self._logical_control = ["F1","F2"]
        self._logical_environment = ["resolution","delta-m","mass","mode-change-delay"]
        self._logical_global = ["F1","F2","resolution","delta-m","mass","mode-change-delay"]
        self._logical_input  = ["inhibit","filok","emok","ptrip","IO1","IO2","IO3","IO4","IO5","Faraday","Total","auxiliary1","auxiliary2", \
                                "clock","mSecs","elapsed-time","watchdog"]
        self._logical_map  = ["mass"]
        self._logical_measurement = ["SEM","Faraday","Total","auxiliary1","auxiliary2"]
        self._logical_mode = ["RGA/SIMS","F1","F2","resolution","delta-m","mass","mode-change-delay"]
        self._logical_others = ["F1","F2"]
        self._logical_output = ["i/p_select","local_range","head_range","trip1","trip2","optrip","emission-LED","fault-LED","RGA/SIMS", \
                                "emissionrange","F1","F2","beam","Faraday_range","Total_range","auxiliary1_range","auxiliary2_range", \
                                "nul_range","resolution","delta-m","mass"]
        self._logical_quad =  ["resolution","delta-m"]
        self._logical_switched = ["total/partial", "multiplier", "1st-dynode"]
        self._logical_raster = ["raster"]
        self._logical_total_partial = ["T/P","mass"]
        self._logical_all = ["state"]
        self._logical_all.extend(self._logical_switched)
        self._logical_all.extend(self._logical_output)
        # self._logical_all.extend(self._logical_rangedev) range devices are excluded from this list
        self._logical_all.extend(self._logical_measurement)
        self._logical_all.extend(self._logical_raster)
        self._initialize_data()

    def _initialize_data(self):
        self.connected = True
        self._scans = {}
        self._current_scan = None
        self._terse = False
        self._min_mass = 1
        self._max_mass = 100
        self._mass = 4
        self._min_energy = 6
        self._max_energy = 100
        self._electron_energy = 70
        self._emission = 100
        self._stopping = False
        self._cycles = 0
        self._interval = 0
        self._points = 70
        self._emok = True
        self._filok = True
        self._ptrip = False
        self._overtemp = False
        self._zero = False
        self._mode = 1
        self._dwell = 100
        self._dwellmode = True
        self._settle = 100
        self._settlemode = True
        self._noise = 1E-9
        self._total_pressure = 0
        self._low = -12
        self._high = -5
        self._terse = True

    def reset(self):
        self._initialize_data()
        
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
    def id(self):
        return "#" + self._name.split("#",1)[1]

    @property
    def release(self):
        return self._release
        

    @property
    def scan_table(self):
        return self._scan_table
        
    @property
    def logical_all(self):
        return self._logical_all
        
    @property
    def logical_groups(self):
        return self._logical_groups

    @property
    def logical_rangedev(self):
        return self._logical_rangedev
        
    @property
    def logical_control(self):
        return self._logical_control
        
    @property
    def logical_environment(self):
        return self._logical_environment
        
    @property
    def logical_global(self):
        return self._logical_global
        
    @property
    def logical_input(self):
        return self._logical_input

    @property
    def logical_map(self):
        return self._logical_map
        
    @property
    def logical_measurement(self):
        return self._logical_measurement
        
    @property
    def logical_mode(self):
        return self._logical_mode
        
    @property
    def logical_others(self):
        return self._logical_others
        
    @property
    def logical_output(self):
        return self._logical_output
        
    @property
    def logical_quad(self):
        return self._logical_quad
        
    @property
    def logical_switched(self):
        return self._logical_switched
        
    @property
    def logical_total_partial(self):
        return self._logical_total_partial
        
    @property
    def terse(self):
        return self._terse

    @terse.setter
    def terse(self, terse):
        self._terse = terse
        
    @property
    def data_queue(self):
        return self.current_scan.data_queue

    def next_data_point(self, current_scan):
        """
        Retrieve one value queued by the scan thread from each queue.
        """
        return_string = ""
        # NB, this isn't the self.current_scan which is used by the aquisition thread.
        scan_point = current_scan.scan_queue.get()
        report = current_scan.report
        if scan_point == current_scan.start:
            time_point = current_scan.time_queue.get()
            return_string += "["
            if (report & 16) != 0:
                return_string += "/" + str(time_point) + "/"
            current_scan.time_queue.task_done()
            return_string += "{"
        for name, other_scan in self._scans.items():
            if other_scan != current_scan:
                if not other_scan.scan_queue.empty():
                    other_scan_point = other_scan.scan_queue.get()
                    if other_scan_point == other_scan.start:
                        other_scan.time_queue.get()
                        other_scan.time_queue.task_done()
                    other_value = other_scan.data_queue.get()
                    print(other_scan.scan_output + " set to " + str(other_scan_point) + " at " + str(other_value))
                    other_scan.data_queue.task_done()
                    other_scan.scan_queue.task_done()
        if (report & 4) != 0:
            return_string += str(scan_point)
            return_string += ":"
        value = current_scan.data_queue.get()
        if (report & 1) != 0:
            if value >= 0:
                return_string += " "
            return_string += str(value)
            return_string += ","
        current_scan.data_queue.task_done()
        if (report & 4) != 0:
            if scan_point >= current_scan.stop:
                return_string += "}]"
        current_scan.scan_queue.task_done()
        return return_string

    def data(self, all=False):
        """
        Retrieves all currently queued data values.
        """
        point = 0
        return_string = ""
        current_scan = None
        for name, scan in self._scans.items():
            if scan.report != 0:
                current_scan = scan
                break
        if current_scan.data_queue.empty() and not self.stat:
            return "*C110*"     # No more data available
            
        while not current_scan.data_queue.empty():
            if self._stopping:
                break
            return_string += self.next_data_point(current_scan)
            point += 1
            if not all and point >= self.points:
                break
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
            self._scans[current_scan] = scanner.Scanner("mass")
        self._current_scan = self._scans[current_scan]

    @property
    def current_row(self):
        if self.current_scan == None:
            return 0
        return self._current_scan.current_row
        
    @current_row.setter
    def current_row(self, current_row):
        self._current_scan.current_row = current_row

    @property
    def rows(self):
        if self.current_scan == None:
            return 0
        return self._current_scan.rows
        
    @property
    def scan_output(self):
        if self.current_scan is None:
            return "mass"
        return self._current_scan.scan_output

    @scan_output.setter
    def scan_output(self, output):
        self._current_scan.scan_output = output

    @property
    def scan_input(self):
        if self.current_scan is None:
            return "Faraday"
        return self._current_scan.scan_input

    @scan_input.setter
    def scan_input(self, input):
        self._current_scan.scan_input = input

    @property
    def min_mass(self):
        return self._min_mass

    @property
    def scan_start(self):
        if self.current_scan is None:
            return 0
        return self._current_scan.start

    @property
    def max_mass(self):
        return self._max_mass

    @property
    def scan_stop(self):
        if self.current_scan is None:
            return self.max_mass
        return self._current_scan.stop

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
    def mass(self):
        return self._mass
        
    @mass.setter
    def mass(self, mass):
        self._mass = mass
        
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
        return self._current_scan.report

    @report.setter
    def report(self, report):
        self._current_scan.report = report

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

    def start(self, current_scan):
        """
        Starts threaded data acquisition.
        """
        if current_scan not in self._scans:
            self._scans[current_scan] = Scanner()
        self._current_scan = self._scans[current_scan]
        self._scan_thread = ScanThread(self, "scan_thread")
        for name, scan in self._scans.items():
            scan.clear_queues()
        self._scan_thread.start()

    @property
    def stat(self):
        if self._scan_thread is None:
            return False
        return self._scan_thread.is_alive()

    def stop(self, stopping=True):
        """
        Stops scanning immediately
        """
        self.log.info("Stop scanning now.")
        self._stopping = stopping
        if self._scan_thread is not None:
            self._scan_thread.join()
        self._scan_thread = None
        
    @property
    def current_row_start(self):
        if self.current_scan == None:
            return 0
        return self.current_scan.current_row_start

    @current_row_start.setter
    def current_row_start(self, current_row_start):
        self.current_scan.current_row_start = current_row_start
    
    @property
    def current_row_stop(self):
        if self.current_scan == None:
            return 0
        return self.current_scan.current_row_stop

    @current_row_stop.setter
    def current_row_stop(self, current_row_stop):
        self.current_scan.current_row_stop = current_row_stop
    
    @property
    def current_row_step(self):
        if self.current_scan == None:
            return 0
        return self.current_scan.current_row_step

    @current_row_step.setter
    def current_row_step(self, current_row_step):
        self.current_scan.current_row_step = current_row_step
        
    def scan_value(self, data_point):
        """
        Acquires one data sample.
        """
        scan_point = self.current_row_start + self.current_row_step * data_point
        time.sleep(self._dwell / 1000.0)
        if self.current_scan.scan_output == "energy":
            self.electron_energy = scan_point
            
        if self.current_scan.scan_output == "mass":
            self.mass = scan_point
        
        signal = 0
        noise = 0
        if self.current_scan.scan_input == "SEM" or self.current_scan.scan_input == "Faraday":
            signal = self._gasses.signal(self.mass, self.electron_energy)
            noise = normal(-self._noise, self._noise)
            if self.current_scan.scan_input == "SEM":
                # Lower noise in SEM mode.
                noise /= 1000
            if self.dwell != 0:
                noise = noise * 100 / self.dwell

        if self.current_scan.scan_input[1:len(self.current_scan.scan_input)] == "scans":
            other_scan = self._scans[self.current_scan.scan_input]
            if other_scan.scan_output == "energy":
                signal = self.electron_energy
            if other_scan.scan_output == "mass":
                signal = self.mass
                
        # Bit 0, return input value. NB, not neccecarily used for report.
        self.current_scan.data_queue.put(signal + noise)
        # Bit 2, output value. NB, not neccecarily used for report.
        self.current_scan.scan_queue.put(scan_point)
    
    def scan_row(self, start_time):
        """
        Scans the current row.
        """
        data_point = 0
        data_points = round((self.current_row_stop - self.current_row_start) / self.current_row_step)
        elapsed = int((time.monotonic() - start_time) * 1000.0)
        # Bit 4, elapsed time in ms. NB, not neccecarily used for report.
        self.current_scan.time_queue.put(elapsed)
        while data_point <= data_points:
            if self._stopping:
                break
            if self.current_scan.scan_input[1:len(self.current_scan.scan_input)] == "scans":
                present_scan = self.current_scan  # Cache current scan reference
                self._current_scan = self._scans[self.current_scan.scan_input]
                self.scan(start_time)  # Recursive!
                self._current_scan = present_scan
            self.scan_value(data_point)
            data_point += 1
            
    def scan(self, start_time):
        for self.current_row, item in enumerate(self._current_scan.rows):
            self.scan_row(start_time)

