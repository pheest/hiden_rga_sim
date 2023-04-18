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
from random import uniform
import time
import threading
import queue
import math


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
            if self._device._cycles != 0:
                cycle += 1

class SimulatedHidenRGA(StateMachineDevice):
    def __init__(self):
        super().__init__()
        self._Ascans = None
    
    def _initialize_data(self):
        self.reset()
        
    def reset(self):
        self.connected = True
        self._name = "HAL RC RGA 201 #13656"
        self._terse = False
        self._min_mass = 1.5
        self._scan_start = self._min_mass
        self._max_mass = 10.5
        self._scan_stop = self._max_mass
        self._scan_step = 0.1
        self._stopping = False
        self._cycles = 0
        self._interval = 0
        self._data_queue = queue.Queue()
        self._points = 70
        self._emok = True
        self._filok = True
        self._ptrip = False
        self._overtemp = False
        self._row = 1
        self._output = "mass"
        self._input = "Faraday"
        self._zero = False
        self._mode = 1
        self._report = 5
        self._dwell = 100
        self._dwellmode = True
        self._settle = 100
        self._settlemode = True
        self._noise = 1E-9

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
        
    def data(self, all=False):
        if self._data_queue.empty():
            if not self.stat:
                return "*C110*"  # No more data available
            else:
                return ""
        qsize = round(math.ceil(self._data_queue.qsize() / 2))
        return_size = qsize
        if not all and return_size > self._points:
            return_size = self._points
        point = 0
        return_string = ""
        while point < return_size:
            scan_point = self._data_queue.get()
            if scan_point == self._scan_start:
                return_string += "["
            return_string += str(scan_point)
            self._data_queue.task_done()
            return_string += ","
            value = self._data_queue.get()
            return_string += str(value)
            self._data_queue.task_done()
            return_string += ","
            if scan_point >= self._scan_stop:
                return_string += "]"
                if not self.stat:
                    return_string != "!"
            point += 1
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
    def row(self):
        return self._row
        
    @row.setter
    def row(self, row):
        self._row = row
        
    @property
    def output(self):
        return self._output
        
    @output.setter
    def output(self, output):
        self._output = output
        
    @property
    def min_mass(self):
        return self._min_mass
        
    @property
    def scan_start(self):
        return self._scan_start
        
    @scan_start.setter
    def scan_start(self, start):
        self._scan_start = start
        
    @property
    def max_mass(self):
        return self._max_mass
        
    @property
    def scan_stop(self):
        return self._scan_stop
        
    @scan_stop.setter
    def scan_stop(self, stop):
        self._scan_stop = stop
        
    @property
    def scan_step(self):
        return self._scan_step
        
    @scan_step.setter
    def scan_step(self, step):
        self._scan_step = step
        
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
        
    def start(self):
        self._Ascans = ScanThread(self, "Ascans")
        self._Ascans.start()
        
    @property
    def stat(self):
        if self._Ascans == None:
            return False
        return self._Ascans.is_alive()
    
    def stop(self):
        """Stops scanning immediately """
        self.log.info("Stop scanning now.")
        self._stopping = True
        if self._Ascans != None:
            self._Ascans.join()
        self._Ascans = None
        
    def scan(self):
        data_point = 0
        data_points = round((self._scan_stop - self._scan_start) / self._scan_step)
        while data_point <= data_points:
            if self._stopping:
                break
            scan_point = self.scan_start + self._scan_step * data_point
            time.sleep(self._dwell / 1000.0)
            noise = uniform(-self._noise, self._noise)
            self._data_queue.put(scan_point)
            self._data_queue.put(noise)
            data_point += 1


if __name__ == '__main__':
    """ For debug purpose only. """
    Simulator = SimulatedHidenRGA()
    Simulator.cycles = 5
    Simulator.scan()
    print(Simulator.data(True))
