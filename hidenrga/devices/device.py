##################################################
#
# Device simulator file for Hiden RGA
#
# Author : P.J. L. Heesterman (Capgemini Engineering)
#
# Copyright (c) : 2023 ITER Organization,
#                 CS 90 046
#                 13067 St. Paul-lez-Durance Cedex
#                 France
#
# This file is part of ITER CODAC software.
# For the terms and conditions of redistribution or use of this software
# refer to the file ITER-LICENSE.TXT located in the top level directory
# of the distribution package.
#
# This file is part implemenation of RGA-SDM-01 "Hardware simulator"
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
from enum import Enum

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


class SimulatedHidenRGA(StateMachineDevice):
    class StopOptions(Enum):
        SCAN = 0
        STOP = 1
        ABORT = 2
        
    class TripError(RuntimeError):
        def __init__(self, code):
            self._code = code
        
        @property
        def code(self):
            return self._code
            
    class ScanThread(threading.Thread):
        def __init__(self, device, name):
            super().__init__()
            self._device = device
            self.name = name

        def run(self):
            """ 
            Thread method to aquire data
            """
            try:
                self._device.log.info("Starting thread")
                cycle = 0
                self._device._stopping = self._device.StopOptions.SCAN
                # Cache these values as they will be overwritten
                mass = self._device.mass
                energy = self._device.energy
                start_time = time.monotonic()
                while self._device.cycles == 0 or cycle < self._device.cycles:
                    if not self._device.scan(start_time):
                        break
                    if self._device._stopping == self._device.StopOptions.STOP:
                        break
                    if self._device.cycles != 0:
                        cycle += 1
            except Exception as Error:
                self._device.log.error(str(Error))
                
            # Restore these values
            self._device.mass = mass
            self._device.energy = energy
            self._device.log.info("Exiting thread")

    class Logical:
        def __init__(self):
            self._groups = {}
            self._groups["ADAM-4017-1"] = ["ADAM-4017-1-range","ADAM-4017-1-type","input1","input2","input3","input4","input5"]
            self._groups["ADAM-4018-1"] = ["ADAM-4018-1-range","ADAM-4018-1-type","temperature1","temperature2","temperature3","temperature4","temperature5"]
            self._groups["ADAM-4050-1"] = ["ADAM-4050-1-type","RI1","RI2","RI3","RI4","RI5","RI6","RI7","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8"]
            
            self._groups["all"] =  ["0V","F1","F1-LED","F2","F2-LED","Faraday","IO1","IO2","IO3","IO4","IO5","IO_all","IO_direction","MFC1","MFC1_flow", \
                                    "N10V24","P3V3","P5V12","PI1","PI2","PI3","PI4","PI5","PI6","PI7","PI8","PO1","PO10","PO2","PO3","PO4","PO5","PO6","PO7","PO8","PO9", \
                                    "RGA-SIMS","RI1","RI2","RI3","RI4","RI5","RI6","RI7","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8","SEM","T-P","Total", \
                                    "VCU1-turbo-power","VCU1-turbo-run-time","VCU1-turbo-speed","VCU1-turbo-temperature","Vacuum","auxiliary1","auxiliary2","beep", \
                                    "cage","channel_1","channel_2","channel_3","channel_4","client-connected","clock","dac1-mon-select","dac1-monitor","dac2-mon-select","dac2-monitor", \
                                    "delay","delta-m","display-error","display-line","electron-energy","electron-energy-DAC","emission","emission-limit","emission-range","emission-value", \
                                    "emok","emsafe","enable","enable-PIA","enable-ext","enabled","f(%%)","f(%)","f(Pa)","f(V)","f(mbar)","f(ppm)","f(torr)","f(x)","fault-LED","filok","focus", \
                                    "head-range","inhibit","input1","input2","input3","input4","input5","ip-select","local-range","mSecs","mass","mass-dac","mass-monitor","mass-range","mass-scale", \
                                    "mode","mode-change-delay","monitor0","monitor1","monitor2","monitor3","multiplier","none","optrip","overtemp","process_read","protection","ptrip","random","rangedev", \
                                    "recovery-mode","remote-io-retries","remote-io-slaves","resn-dac","resn-monitor","resolution","rfdc-monitor","run-LED","scan","scanning", \
                                    "shutdown","shutdown-req","state","temperature1","temperature2","temperature3","temperature4","temperature5","testpoint","timer", \
                                    "trip1","trip2","turbo-power","turbo-run-time","turbo-speed","turbo-temperature","uptime","vacuum","watchdog","watchdog-active"]            
            self._groups["MFC"] = ["MFC"]
            self._groups["MFC-1"] = ["MFC1","MFC1_flow"]
            self._groups["MSC08-VCU-protocol"] = ["VCU1"]
            self._groups["MSC10-Modbus"] = ["ADAM-4017-1","ADAM-4018-1","ADAM-4050-1","MFC-1"]
            self._groups["MSC10-Modbus"] = ["ADAM-4017-1","ADAM-4018-1","ADAM-4050-1","MFC-1"]
            self._groups["SEMHT"] = ["multiplier"]
            self._groups["VCU1"] = ["VCU1-ADC-calibration","VCU1-AIM-on-point","VCU1-Aux24V-control","VCU1-assign_setpoint1","VCU1-assign_setpoint2","VCU1-assign_setpoint3", \
                                    "VCU1-degas-gauges","VCU1-enable_setpoint1","VCU1-enable_setpoint2","VCU1-enable_setpoint3","VCU1-pressure-unit", \
                                    "VCU1-setpoint1_high","VCU1-setpoint1_low","VCU1-setpoint2_high","VCU1-setpoint2_low","VCU1-setpoint3_high", \
                                    "VCU1-setpoint3_low","VCU1-turbo-factory-reset","VCU1-turbo-power","VCU1-turbo-power-setting","VCU1-turbo-run-time", \
                                    "VCU1-turbo-speed","VCU1-turbo-temperature","VCU1-turbo-type","Vacuum","turbo-power","turbo-power-setting","turbo-run-time" \
                                    ,"turbo-speed","turbo-temperature","vacuum"]
            self._groups["analogue-out"] = ["channel_1","channel_2","channel_3","channel_4"]
            self._groups["beam"] = ["cage"]
            self._groups["degas"] = ["beam","electron-energy","emission"]
            self._groups["detector"] = ["multiplier"]
            self._groups["enable"] = ["F1","F2","enable-PIA","shutdown","switched"]
            self._groups["environment"] = ["MFC1","cage","channel_1","channel_2","channel_3","channel_4","delta-m","electron-energy","emission","focus","mass","mode-change-delay","resolution"]
            self._groups["filter"] = ["focus"]

            self._groups["control"] = ["F1","F2"]
            self._groups["environment"] = ["resolution","delta-m","mass","mode-change-delay"]
            self._groups["global"] = ["F1","F2","MFC1","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8","cage","channel_1","channel_2","channel_3","channel_4", \
                                      "delta-m","electron-energy","emission","focus","mass","mode-change-delay","multiplier","resolution"]
            self._groups["input"] = ["0V","Faraday","IO1","IO2","IO3","IO4","IO5","IO_all","MFC1_flow","N10V24","P3V3","P5V12","PI1","PI2","PI3","PI4","PI5","PI6","PI7", \
                                     "PI8","RI1","RI2","RI3","RI4","RI5","RI6","RI7","SEM","Total","VCU1-turbo-power","VCU1-turbo-run-time","VCU1-turbo-speed", \
                                     "VCU1-turbo-temperature","Vacuum","auxiliary1","auxiliary2","client-connected","clock","emission-limit","emok","emsafe","enabled", \
                                     "f(%%)","f(%)","f(Pa)","f(V)","f(mbar)","f(ppm)","f(torr)","f(x)","filok","inhibit","input1","input2","input3","input4","input5", \
                                     "mSecs","ms-count","none","overtemp","process_read","ptrip","scanning","shutdown-req","temperature1","temperature2","temperature3","temperature4","temperature5", \
                                     "turbo-power","turbo-run-time","turbo-speed","turbo-temperature","uptime","vacuum","watchdog"]
                                     
            self._groups["main"] = ["F1","F2","MFC1","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8","cage","channel_1","channel_2","channel_3","channel_4","delta-m", \
                                    "electron-energy","emission","focus","mass","mode-change-delay","multiplier","resolution"]
            self._groups["map"] = ["electron-energy","f(%%)","f(%)","f(V)","f(mbar)","f(ppm)","f(x)","focus","mass","none"]
            self._groups["measurement"] = ["Faraday","MFC1_flow","SEM","Total","auxiliary1","auxiliary2","f(%%)","f(%)","f(V)","f(mbar)","f(ppm)","f(x)","input1","input2","input3","input4","input5", \
                                           "none","temperature1","temperature2","temperature3","temperature4","temperature5","vacuum"]
            self._groups["measurement"] = ["Faraday","MFC1_flow","SEM","Total","auxiliary1","auxiliary2","f(%%)","f(%)","f(V)","f(mbar)","f(ppm)","f(x)","input1","input2","input3","input4","input5", \
                                           "none","temperature1","temperature2","temperature3","temperature4","temperature5","vacuum"]
                                           
            self._groups["mode"] = ["F1","F2","MFC1","RGA-SIMS","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8","cage","channel_1","channel_2","channel_3","channel_4","delta-m","electron-energy","emission", \
                                   "focus","mass","mode-change-delay","multiplier","resolution"]
            self._groups["monitorable"] = ["0V","F1","F2","IO1","IO2","IO3","IO4","IO5","IO_all","MFC1_flow","N10V24","P3V3","P5V12","PI1","PI2","PI3","PI4","PI5","PI6","PI7","PI8", \
                                           "RI1","RI2","RI3","RI4","RI5","RI6","RI7","VCU1-turbo-power","VCU1-turbo-run-time","VCU1-turbo-speed","VCU1-turbo-temperature", \
                                           "Vacuum","cage","clock","delta-m","electron-energy","emission","emok","emsafe","enabled","filok","focus","inhibit", \
                                           "input1","input2","input3","input4","input5","mSecs","mass","mode-change-delay","ms-count","multiplier","overtemp", \
                                           "process_read","ptrip","resolution","scanning","shutdown-req","temperature1","temperature2","temperature3","temperature4","temperature5", \
                                           "turbo-power","turbo-run-time","turbo-speed","turbo-temperature","uptime"]
            self._groups["others"] = ["F1","F2"]
            self._groups["output"] = ["F1","F2","Faraday_range","IO1","IO2","IO3","IO4","IO5","IO_all","IO_direction","MFC1","PO1","PO10","PO2","PO3","PO4","PO5","PO6","PO7","PO8","PO9", \
                                      "RGA-SIMS","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8","SEM_range","Total_range","auxiliary1_range","auxiliary2_range","beep","cage", \
                                      "channel_1","channel_2","channel_3","channel_4","delay","delta-m","electron-energy","electron-energy-DAC","emission","enable-ext","enable-leds", \
                                      "fault-LED","focus","head-range","local-range","mass","mass-dac","mass-scale","multiplier","none_range","nul_range","optrip",
                                      "process_write","resn-dac","resolution","rmon-en","testpoint","timer","trip1","trip2"]
            self._groups["quad"] =  ["resolution","delta-m"]
            self._groups["rangedev"] =  ["Faraday_range","SEM_range","Total_range","auxiliary1_range","auxiliary2_range","none_range","nul_range"]
            self._groups["remote-io-items"] =  ["ADAM-4017-1-range","ADAM-4017-1-type","ADAM-4018-1-range","ADAM-4018-1-type","ADAM-4050-1-type","MFC1","MFC1_flow", \
                                                "RI1","RI2","RI3","RI4","RI5","RI6","RI7","RO1","RO2","RO3","RO4","RO5","RO6","RO7","RO8","VCU1-ADC-calibration", \
                                                "VCU1-AIM-on-point","VCU1-Aux24V-control","VCU1-assign_setpoint1","VCU1-assign_setpoint2","VCU1-assign_setpoint3", \
                                                "VCU1-degas-gauges","VCU1-enable_setpoint1","VCU1-enable_setpoint2","VCU1-enable_setpoint3","VCU1-pressure-unit", \
                                                "VCU1-setpoint1_high","VCU1-setpoint1_low","VCU1-setpoint2_high","VCU1-setpoint2_low","VCU1-setpoint3_high","VCU1-setpoint3_low", \
                                                "VCU1-turbo-factory-reset","VCU1-turbo-power","VCU1-turbo-power-setting","VCU1-turbo-run-time","VCU1-turbo-speed", \
                                                "VCU1-turbo-temperature","VCU1-turbo-type","Vacuum","input1","input2","input3","input4","input5", \
                                                "temperature1","temperature2","temperature3","temperature4","temperature5", \
                                                "turbo-power","turbo-power-setting","turbo-run-time","turbo-speed","turbo-temperature","vacuum"]
            self._groups["remote-io-masters"] =  ["MSC08-VCU-protocol","MSC10-Modbus"]
            self._groups["remote-io-slaves"] =  ["ADAM-4017-1","ADAM-4018-1","ADAM-4050-1","MFC-1","VCU1"]
            self._groups["root"] =  ["main"]
            self._groups["shutdown"] =  ["RGA-SIMS","cage","delta-m","electron-energy","emission","focus","mode-change-delay","resolution"]
            self._groups["source"] =  ["cage","electron-energy","emission"]
            self._groups["test"] =  ["dac1-mon-select","dac1-monitor","dac2-mon-select","dac2-monitor","mass-dac","mass-monitor",
                                     "monitor0","monitor1","monitor2","monitor3","resn-dac","resn-monitor","rfdc-monitor","testpoint","zm1-led1"]
            self._groups["switched"] = ["SEMHT","total-partial"]
            self._groups["total-partial"] = ["T-P","mass"]
            self._groups["tune-group"] = ["MFC", "detector","filter","quad","source"]
            self._scan_table = ["scan","row","cycles","interval","state","output","start","stop","step","input","rangedev","low", \
                                "high","current","zero","dwell","settle","mode","report","options","return","type","env"]
        
        @property
        def groups(self):
            return self._groups
            
        @property
        def all(self):
            return self._groups["all"]
            
        @property
        def scan_table(self):
            return self._scan_table
        
    def __init__(self):
        super().__init__()
        self._scan_thread = None
        self._gasses = gasses.Gasses()
        self._current_gas = None
        self._name = "HAL RC RGA 101X #17995"
        self._release = "Release 10.11.0, 2022-11-28, 131720"
        self._configuration = "WRD17995#cnfa.xml, 2023-03-16, 08:01, HAL10, Internal RGA 201 R10.11.0, 6d6ef24f"
        self._logical = self.Logical()
        self._initialize_data()

    def __del__(self):
        self.join(None)
        
    def _initialize_data(self):
        self.connected = True
        self._enable = False
        self._scans = {}
        self._current_scan = None
        self._terse = False
        self._min_mass = 1
        self._max_mass = 200
        self._mass = 4
        self._min_energy = 6
        self._max_energy = 100
        self._energy = 70
        self._emission = 0
        self._stopping = self.StopOptions.SCAN
        self._nowait = threading.Event()
        self._nowait.set()
        self._cycles = 0
        self._interval = 0
        self._points = 70
        self._F1 = False
        self._F2 = False
        self._emok = False
        self._filok = False
        self._ptrip = False
        self._overtemp = False
        self._inhibit = False
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

    def sdel_all(self):
        self._scans = {}
        self._current_scan = None
        
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
    def release(self):
        return self._release
        

    @property
    def configuration(self):
        return self._configuration
        
    @property
    def scan_table(self):
        return self._logical.scan_table
        
    @property
    def logical_all(self):
        return self._logical.all
        
    @property
    def logical_groups(self):
        return self._logical.groups
        
    def logical_group(self, group):
        return self._logical.groups[group]
        
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
            return_string += "["
        for current_row in range(0, len(current_scan.rows)):
            if scan_point == current_scan.rows[current_row].start:
                time_point = current_scan.time_queue.get()
                if (report & 16) != 0:
                    return_string += "/" + str(time_point) + "/"
                current_scan.time_queue.task_done()
        if scan_point == current_scan.start:
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
        value = current_scan.data_queue.get()
        if isinstance(value, self.TripError):
            return_string += "*P" + str(value.code) + "*"
        else:
            if (report & 4) != 0:
                return_string += str(scan_point)
                return_string += ":"
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
        self.join(0)
        return self._emok

    @emok.setter
    def emok(self, emok):
        self._emok = emok

    @property
    def filok(self):
        self.join(0)
        return self._filok

    @filok.setter
    def filok(self, filok):
        self._filok = filok
        if not filok:
            self._emok = False

    @property
    def ptrip(self):
        self.join(0)
        return self._ptrip

    @property
    def overtemp(self):
        self.join(0)
        return self._overtemp

    @overtemp.setter
    def overtemp(self, overtemp):
        self._overtemp = overtemp

    @property
    def inhibit(self):
        self.join(0)
        return self._inhibit

    @inhibit.setter
    def inhibit(self, inhibit):
        self._inhibit = inhibit

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
        if self.current_scan is None:
            return 0
        return self._current_scan.current_row
        
    @current_row.setter
    def current_row(self, current_row):
        self._current_scan.current_row = current_row

    @property
    def rows(self):
        if self.current_scan is None:
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
    def energy(self):
        return self._energy
        
    @energy.setter
    def energy(self, energy):
        self._energy = energy
        
    @property
    def enable(self):
        return self._enable
        
    @enable.setter
    def enable(self, enable):
        self._enable = (enable == 1)
        
    @property
    def F1(self):
        return self._F1
        
    @F1.setter
    def F1(self, F1):
        self._F1 = (F1 == 1)
        if self._F1 or self._F2:
            self._filok = True
            self._emok = True
        elif self._emission > 0:
            self._filok = False
            self._emok = False
        
    @property
    def F2(self):
        return self._F2
        
    @F2.setter
    def F2(self, F2):
        self._F2 = (F2 == 1)
        if self._F1 or self._F2:
            self._filok = True
            self._emok = True
        elif self._emission > 0:
            self._filok = False
            self._emok = False
        
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
            
        self._total_pressure += partial_pressure - self._gasses.gas(self._current_gas).partial_pressure
        if self._total_pressure > 1E-2: # NB, Pascal units
            self.log.warning("Total pressure caused trip at " + str(self._total_pressure))
            self._ptrip = True
            self._emission = 0
            self._scan_input = "Faraday"
        elif self._ptrip:
            self.log.info("Pressure trip cleared with " + str(self._total_pressure))
            self._ptrip = False
        
        self._gasses.gas(self._current_gas).partial_pressure = partial_pressure
        self.log.info(str(self._current_gas) + " pressure set to " + str(self._gasses.gas(self._current_gas).partial_pressure) + " total now " + str(self._total_pressure))
        
    @property
    def total_pressure(self):
        return self._total_pressure
        
    def join(self, timeout):
        if self._scan_thread is not None:
            self._scan_thread.join(timeout)
            if not self._scan_thread.is_alive():
                self.log.info("Thread has exitied.")
                self._scan_thread = None

    def start(self, current_scan):
        """
        Starts threaded data acquisition.
        """
        if self._scan_thread is not None:
            self.log.warning("Thread was still active, stopping.")
            self._scan_thread.join(None)
            self._scan_thread = None
        
        if current_scan not in self._scans:
            self._scans[current_scan] = Scanner()
        self._current_scan = self._scans[current_scan]
        self._scan_thread = self.ScanThread(self, "scan_thread")
        for name, scan in self._scans.items():
            scan.clear_queues()
        self._scan_thread.start()

    @property
    def stat(self):
        if self._scan_thread is None:
            return False
        return self._scan_thread.is_alive()

    def stop(self, stopping=StopOptions.ABORT):
        """
        Stops scanning immediately
        """
        self.log.info("Stop scanning now.")
        timeout = None
        if stopping:
            self._stopping = self.StopOptions.ABORT
        else:
            self._stopping = self.StopOptions.STOP
            timeout = 0
        self._nowait.set()
        self.join(timeout)

    @property
    def wait(self):
        return not self._nowait.is_set()
        
    @wait.setter
    def wait(self, wait):
        if wait:
            self.log.info("Pause scanning at end of cycle.")
            self._nowait.clear()
        else:
            self.log.info("Continue scanning at end of cycle.")
            self._nowait.set()
        
    @property
    def current_row_start(self):
        if self.current_scan is None:
            return 0
        return self.current_scan.current_row_start

    @current_row_start.setter
    def current_row_start(self, current_row_start):
        self.current_scan.current_row_start = current_row_start
    
    @property
    def current_row_stop(self):
        if self.current_scan is None:
            return 0
        return self.current_scan.current_row_stop

    @current_row_stop.setter
    def current_row_stop(self, current_row_stop):
        self.current_scan.current_row_stop = current_row_stop
    
    @property
    def current_row_step(self):
        if self.current_scan is None:
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
            self.energy = scan_point
            
        if self.current_scan.scan_output == "mass":
            self.mass = scan_point
        
        signal = 0
        noise = 0
        if self.current_scan.scan_input == "SEM" or self.current_scan.scan_input == "Faraday":
            pascal_to_torr = 0.00750062
            signal = self._gasses.signal(self.mass, self.energy)
            # NB, The Hiden device uses Torr as the output unit.
            # But this project uses Pascal (the SI unit) as the unit wherever possible.
            signal *= pascal_to_torr
            noise = normal(-self._noise, self._noise)
            if self.current_scan.scan_input == "SEM":
                # Lower noise in SEM mode.
                noise /= 1000
            if self.dwell != 0:
                noise = noise * 100 / self.dwell

        if self.current_scan.scan_input[1:len(self.current_scan.scan_input)] == "scans":
            other_scan = self._scans[self.current_scan.scan_input]
            if other_scan.scan_output == "energy":
                signal = self.energy
            if other_scan.scan_output == "mass":
                signal = self.mass
        
        TripError = None
        if self._inhibit:
            self.log.warning("inhibit is set")
            TripError = self.TripError(111)
        elif self._ptrip:
            self.log.warning("ptrip is set")
            TripError = self.TripError(112)
        elif not self._filok:
            self.log.warning("filok is not set")
            TripError = self.TripError(113)
        elif not self._emok:
            self.log.warning("emok is not set")
            TripError = self.TripError(114)
        elif self._overtemp:
            self.log.warning("overtemp is set")
            TripError = self.TripError(115)
            
        if TripError is None:
            # Bit 0, return input value. NB, not neccecarily used for report.
            self.current_scan.data_queue.put(signal + noise)
        else:
            # Send trip error
            self.current_scan.data_queue.put(TripError)
        
        # Bit 2, output value. NB, not neccecarily used for report.
        self.current_scan.scan_queue.put(scan_point)
        return TripError is None
    
    def scan_row(self, start_time):
        """
        Scans the current row.
        """
        data_point = 0
        
        value_tolerance = sys.float_info.epsilon * (1 + self.current_row_stop)
        
        current_row_length = self.current_row_stop - self.current_row_start
        
        if abs(current_row_length) < value_tolerance:
            data_points = 1
            self.log.info("Zero row length, setting 1 point with " + str(self.current_row_step) + " step")
        else:
            data_points = int(0.5 + float(current_row_length) / self.current_row_step)
            self.log.debug("Finite row length, setting " + str(data_points) + " points")
        elapsed = int((time.monotonic() - start_time) * 1000.0)
        # Bit 4, elapsed time in ms. NB, not neccecarily used for report.
        self.current_scan.time_queue.put(elapsed)
        while data_point < data_points:
            if data_points == 1:
                self.log.info("Data point")            
            if self._stopping == self.StopOptions.ABORT:
                self.log.warning("Scan aborted by IOC")
                return False
            if self.current_scan.scan_input[1:len(self.current_scan.scan_input)] == "scans":
                present_scan = self._current_scan  # Cache current scan reference
                self._current_scan = self._scans[self.current_scan.scan_input]
                self.scan(start_time)  # Recursive!
                self._current_scan = present_scan
            if not self.scan_value(data_point):
                self.log.warning("Aborting scan due to trip")
                return False
            data_point += 1
        return True
            
    def scan(self, start_time):
        for self.current_row, item in enumerate(self._current_scan.rows):
            if not self.scan_row(start_time):
                return False
        self._nowait.wait()
        return True

