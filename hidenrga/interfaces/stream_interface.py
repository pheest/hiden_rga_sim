##################################################
#
# Stream interface file for Hiden RGA device
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
##################################################

from lewis.adapters.stream import Cmd, StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply
from lewis.core.logging import has_log
import time


class HidenRGAStreamInterface(StreamInterface):
    """
    TCP-stream based Hiden RGA interface
    """
    
    commands = {
        CmdBuilder("get_name").escape("pget name ").build(),
        CmdBuilder("get_name").escape("pget name").build(),
        CmdBuilder("get_name").escape("pget ID").build(),
        CmdBuilder("get_name").escape("pget ID ").build(),
        CmdBuilder("get_release").escape("pget release ").build(),
        CmdBuilder("get_configurationid").escape("pid# configuration ").build(),
        CmdBuilder("get_configurationid").escape("pget configuration ").build(),
        CmdBuilder("sdel_all").escape("sdel all").build(),
        CmdBuilder("set_out").escape("sout").string().build(),
        CmdBuilder("set_err").escape("serr").string().build(),
        CmdBuilder("set_terse").escape("pset terse ").int().build(),
        CmdBuilder("lset").escape("lset ").string().escape(" ").float().build(),
        CmdBuilder("lput").escape("lput ").string().escape(" ").float().build(),
        CmdBuilder("sjob_lput").escape("sjob lput ").string().float().escape(" ").float().build(),
        CmdBuilder("sjob_lget").escape("sjob lget ").string().build(),
        CmdBuilder("sjob_sdel_all").escape("sjob sdel all").build(),
        CmdBuilder("sjob_lset").escape("sjob lset").string().build(),
        CmdBuilder("sjob_quit").escape("sjob quit").build(),
        CmdBuilder("sjob_lini").escape("sjob lini ").string().build(),
        CmdBuilder("sjob_save").escape("sjob save ").build(),
        CmdBuilder("stat_job").escape("stat ").int().build(),
        CmdBuilder("stat_task").escape("stat task ").int().build(),
        CmdBuilder("lget_device").escape("lget ").string().build(),
        CmdBuilder("data_on").escape("data on").build(),
        CmdBuilder("data_all").escape("data all").build(),
        CmdBuilder("data_off").escape("data off").build(),
        CmdBuilder("data").escape("data").build(),
        CmdBuilder("pset_points").escape("pset points ").int().build(),
        CmdBuilder("stop").escape("stop ").string().build(),
        CmdBuilder("sset_scan").escape("sset scan ").string().build(),
        CmdBuilder("lini_scan").escape("lini ").string().build(),
        CmdBuilder("sset_row").escape("sset row ").int().build(),
        CmdBuilder("sset_output").escape("sset output ").string().build(),
        CmdBuilder("sset_start").escape("sset start ").float().build(),
        CmdBuilder("sset_stop").escape("sset stop ").float().build(),
        CmdBuilder("sset_step").escape("sset step ").float().build(),
        CmdBuilder("sset_cycles").escape("sset cycles ").int().build(),
        CmdBuilder("pset_cycles").escape("pset cycles ").int().build(),
        CmdBuilder("sset_interval").escape("sset interval ").int().build(),
        CmdBuilder("sset_input").escape("sset input ").string().build(),
        CmdBuilder("sset_low").escape("sset low ").int().build(),
        CmdBuilder("sset_high").escape("sset high ").int().build(),
        CmdBuilder("sset_current").escape("sset current ").int().build(),
        CmdBuilder("sset_zero").escape("sset zero ").int().build(),
        CmdBuilder("sset_options").escape("sset options ").string().build(),
        CmdBuilder("sset_report").escape("sset report ").int().build(),
        CmdBuilder("sset_dwell").escape("sset dwell ").string().build(),
        CmdBuilder("sset_settle").escape("sset settle ").string().build(),
        CmdBuilder("sjob_sset_mode").escape("sjob sset mode ").int().build(),
        CmdBuilder("sset_mode").escape("sset mode ").int().build(),
        CmdBuilder("tdel_all").escape("tdel all").build(),
        CmdBuilder("quit").escape("quit").build(),
        CmdBuilder("sset_state").escape("sset state ").string().build(),
        CmdBuilder("sval").escape("sval").build(),
        CmdBuilder("l999_scan").escape("l999 scan").build(),
        CmdBuilder("lmin").escape("lmin ").string().build(),
        CmdBuilder("lmax").escape("lmax ").string().build(),
        CmdBuilder("lres").escape("lres ").string().build(),
        CmdBuilder("lid_hash").escape("lid# ").string().build(),
        CmdBuilder("lid_dollar").escape("lid$ ").string().build(),
        CmdBuilder("ltyp").escape("ltyp ").string().build(),
        CmdBuilder("smax_interval").escape("smax interval ").build(),
        CmdBuilder("lunt").escape("lunt ").string().build(),
        CmdBuilder("luse").escape("luse ").int().build(),
        CmdBuilder("lval").escape("lval ").int().build(),
        CmdBuilder("rbuf").escape("rbuf ").build(),
        CmdBuilder("rerr").escape("rerr").build(),
        CmdBuilder("eid_dollar").escape("eid$").int().build(),
    }

    in_terminator = "\r"
    out_terminator = "\r\n"
    
    @conditional_reply("connected")
    def get_name(self):
        return self.device.name
        
    @conditional_reply("connected")
    def get_release(self):
        return self.device.release

    @conditional_reply("connected")
    def get_configurationid(self):
        return 2

    @conditional_reply("connected")
    def get_configuration(self):
        return ""

    @conditional_reply("connected")
    def sdel_all(self):
        self.device.sdel_all()
        return "" #OK
        
    @conditional_reply("connected")
    def set_terse(self, terse):
        """
        Sets the device terse mode.
        """
        self.device.terse = bool(terse)
        return ""  # OK
        
    @conditional_reply("connected")
    def set_out(self, out):
        """
        Sets the device stdout stream.
        """
        return ""  # OK
        
    @conditional_reply("connected")
    def set_err(self, err):
        """
        Sets the device stderr stream.
        """
        return ""  # OK
        
    @conditional_reply("connected")
    def sjob_sdel_all(self):
        self.sdel_all()
        return "task 1, job 1," # Task <task#>, job <job#>,
        
    @conditional_reply("connected")
    def lset(self, device, val):
        if device == 'enable':
            self.device.enable = int(round(val))
        if device == "delay":
           time.sleep(val / 1000)
        #if device == "cage":
            #self.device.cage = val
        if device == "F1":
            self.device.F1 = int(round(val))
        if device == "F2":
            self.device.F2 = int(round(val))
        #if device == "delta-m":
            #self.device.delta-m = val
        if device == "energy":
            self.device.energy = val
        if device == "emission":
            self.device.emission = val
        #if device = "focus":
            #self.device.focus = val
        if device == "mass":
            self.device.mass = val
        #if device = "mode-change-delay":
            #self.device.mode-change-delay = val
        #if device = "multiplier":
            #self.device.multiplier = val
        #if device = "resolution":
            #self.device.resolution = val
        return "" # OK
        
    @conditional_reply("connected")
    def sjob_lset(self, job):
        return "task 1, job 1," # Task <task#>, job <job#>,
        
    @conditional_reply("connected")
    def sjob_quit(self):
        if self.device.stat:
            self.device.stop()
        return "task 1, job 1," # Task <task#>, job <job#>,
        
    @conditional_reply("connected")
    def stop(self, any):
        if self.device.stat:
            self.device.cycles = 1
        return ""  # OK
                
    @conditional_reply("connected")
    def sjob_lini(self, job):
        return "task 1, job 1," # Task <task#>, job <job#>,
        
    @conditional_reply("connected")
    def sjob_lget(self, scan):
        self.device.start(scan)
        return "task 1, job 1," # Task <task#>, job <job#>,

    @conditional_reply("connected")
    def sjob_save(self):
        return "task 1, job 1," # Task <task#>, job <job#>,

    @conditional_reply("connected")
    def lini_scan(self, scan):
        self._device.current_scan = scan
        return ""  # OK

    @conditional_reply("connected")
    def lput(self, device, val0, val1):
        self.lset(device, val1)
        return ""  # OK
    
    @conditional_reply("connected")
    def sjob_lput(self, device, val0, val1):
        self.lput(device, val0, val1)
        return "task 1, job 1,"  # Task <task#>, job <job#>,
        
    @conditional_reply("connected")
    def stat_job(self, job):
        """
        where <status> is "running", "idle" or "stopped"
        """
        stat = "idle"
        if self.device.stat:
            stat = "running"
        return "task "+str(job)+","+stat    # Task n,<status>,[job <job#>, <command>,]
        
    @conditional_reply("connected")
    def stat_task(self, task):
        """
        where <status> is "running", "idle" or "stopped"
        """
        stat = "idle"
        if self.device.stat:
            stat = "running"
        return "task "+str(task)+","+stat    # Task n,<status>,[job <job#>, <command>,]
        
    @conditional_reply("connected")
    def lget_device(self, device):
        retval = "0"
        if device == 'enable' and self.device.enable:
            retval = "1"
        if device == 'energy':
            retval = str(self.device.energy)
        if device == 'emok' and self.device.emok:
            retval = "1"
        if device == 'filok' and self.device.filok:
            retval = "1"
        if device == 'ptrip' and self.device.ptrip:
            retval = "1"
        if device == 'overtemp' and self.device.overtemp:
            retval = "1"
        if device == 'inhibit' and self.device.inhibit:
            retval = "1"
        if device == 'F1' and self.device.F1:
            retval = "1"
        if device == 'F2' and self.device.F2:
            retval = "1"
        return retval             # ( terse = 1 ) <READING>
        
    @conditional_reply("connected")
    def sset_scan(self, scan):
        self._device.current_scan = scan
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_row(self, row):
        # NB, Hiden indexes rows starting at 1. I prefer to index from 0.
        self.device.current_row = row-1
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_output(self, output):
        self.device.scan_output = output
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_start(self, start):
        self.device.current_row_start = start
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_stop(self, stop):
        self.device.current_row_stop = stop
        return ""  # OK
                
    @conditional_reply("connected")
    def sset_step(self, step):
        self.device.current_row_step = step
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_cycles(self, cycles):
        self.device.cycles = cycles
        return ""  # OK
        
    @conditional_reply("connected")
    def pset_cycles(self, cycles):
        # This parameter is now obsolete. PSET cycles n is equivalent to SSET cycles n for Ascans.
        self.device.cycles = cycles
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_interval(self, interval):
        self.device.interval = interval
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_input(self, input):
        self.device.scan_input = input
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_low(self, low):
        self.device.low = low
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_high(self, high):
        self.device.high = high
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_current(self, current):
        self.device.current = current
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_zero(self, zero):
        self.device.zero = bool(zero)
        return ""  # OK
        
    @conditional_reply("connected")
    def sset_options(self, options):
        self.device.options = options
        return ""  # OK
    
    @conditional_reply("connected")
    def sset_report(self, report):
        self.device.report = report
        return ""  # OK
    
    @conditional_reply("connected")
    def sset_dwell(self, dwell):
        # Either e.g. 100 (time in ms) or eg 100% (percent of default value)
        dwellmode = dwell[len(dwell)-1]=='%'
        if dwellmode:
            self.device.dwell = float(dwell[:-1])
        else:
            self.device.dwell = float(dwell)
        self.device.dwellmode = dwellmode
        return ""  # OK
    
    @conditional_reply("connected")
    def sset_settle(self, settle):
        # Either e.g. 100 (time in ms) or eg 100% (percent of default value)
        settlemode = settle[len(settle)-1]=='%'
        if settlemode:
            self.device.settle = float(settle[:-1])
        else:
            self.device.settle = float(settle)
        self.device.settlemode = settlemode
        return ""  # OK
        
    def smax_interval(self):
        return 86400.000
    
    @conditional_reply("connected")
    def sset_mode(self, mode):
        self.device.mode = mode
        return ""  # OK
        
    @conditional_reply("connected")
    def sjob_sset_mode(self, mode):
        self.sset_mode(mode)
        return "task 1, job 1," # Task <task#>, job <job#>,
       
    @conditional_reply("connected")
    def data_on(self):
        """
        Enables data return.
        """
        return ""  # OK
    
    @conditional_reply("connected")
    def data_off(self):
        """
        Disables data return.
        """
        return ""  # OK
    
    @conditional_reply("connected")
    def data_all(self):
        """
        Returns all of the current data string.
        """
        return self.device.data(True)
    
    @conditional_reply("connected")
    def data(self):
        """
        Returns the current data string.
        """
        return self.device.data(False)
    
    @conditional_reply("connected")
    def pset_points(self, points):
        self.device.points = points
        return ""  # OK

    @conditional_reply("connected")
    def quit(self):
        return ""  # OK
    
    @conditional_reply("connected")
    def sset_state(self, state):
        
        if state == 'Abort:':
            if self.device.stat:
                self.device.stop(True)
        if state == 'Stop:':
            if self.device.stat:
                self.device.stop(False)
        if state == 'Wait:':
            self.device.wait = True
        if state == '':
            self.device.wait = False
        return ""  # OK

    @conditional_reply("connected")
    def sval(self):
        return ""  # OK
    
    @conditional_reply("connected")
    def l999_scan(self):
        return ""  # OK
    
    @conditional_reply("connected")
    def tdel_all(self):
        return ""  # OK

    @conditional_reply("connected")
    def lmin(self, logical_device):
        if logical_device == "mass":
            return self.device.min_mass
        if logical_device == "Faraday_range":
            return 1E-11
        return 0
    
    @conditional_reply("connected")
    def lmax(self, logical_device):
        if logical_device.isnumeric():
            logical_index = int(logical_device)
            logical_device = self.logical_device(logical_index)
        if logical_device == "mass":
            return self.device.max_mass
        if logical_device == "Faraday_range":
            return 1E-5
        if logical_device == "emission":
            return 5000
        if logical_device == "Faraday_range":
            return 1E-5
        return 0
    
    @conditional_reply("connected")
    def lres(self, logical_device):
        return 0.001
        
    @conditional_reply("connected")
    def lid_hash(self, logical_device):
        if logical_device not in self.device.logical_all:
            self.log.warn("device not found")
            return 0
        return self.device.logical_all.index(logical_device)
    
    @conditional_reply("connected")
    def lid_dollar(self, logical_device):
        return_value = '"'
        if logical_device == "all":
            return_value += '","'.join(self.device.logical_all)
        elif logical_device == "groups":
            return_value += '","'.join(self.device.logical_groups)
        else:
            return_value += '","'.join(self.device.logical_group(logical_device))
        return_value += '",'
        return return_value
    
    @conditional_reply("connected")
    def ltyp(self, logical_device):
        if logical_device in self.device.logical_groups:
            return "group"
        print("ltyp " + logical_device)
        if logical_device.isnumeric():
            logical_index = int(logical_device)
            logical_device = self.logical_index(logical_index)
        for logical_group in self.device.logical_groups.keys():
            if logical_group != 'all':
               if logical_device in self.device.logical_groups[logical_group]:
                   return logical_group
        return "unknown"
        
    def logical_device(self, logical_index):
        logical_device = "unknown"
        if logical_index < len(self.device.logical_all):
            logical_device = self.device.logical_all[logical_index]
        self.log.info("logical device " + logical_device)
        return logical_device
    
        
    @conditional_reply("connected")
    def luse(self, logical_index):
        return self.logical_device(logical_index)
    
    @conditional_reply("connected")
    def rerr(self):
        return ""  # OK
    
    @conditional_reply("connected")
    def eid_dollar(self, err_no):
        """ Returns the error message relating to the error code """
        return str(err_no)

    @conditional_reply("connected")
    def lunt(self, logical_device):
        if logical_device == "mode":
            return 1   # RGA
        return ""
        
    @conditional_reply("connected")
    def lval(self, logical_index):
        logical_device = self.logical_device(logical_index)
            
        if logical_device in ["Total_range", "Faraday_range"]:
            return "0, -5,0,0,0,0,0,0,0, 0,0,"
        if logical_device in ["SEM_range"]:
            return "0, -7,0,0,0,0,0,0,0, 0,0,"
        if logical_device in ["watchdog-active", "scan", "remote-io-slaves", "emsafe", "client-connected"] :
            return "0, 1,0,0,0,0,0,0,0, 0,0,"
        if logical_device in ["uptime"]:
            return "0, 0d 0h 0m 0s,0d 0h 0m 0s,0d 0h 0m 0s,0d 0h 0m 0s,0d 0h 0m 0s,0d 0h 0m 0s,0d 0h 0m 0s,0d 0h 0m 0s, 0,0,"
        if logical_device in ["testpoint", "ip-select"]:
            return "0, 4,0,0,0,0,0,0,0, 0,0,"
        if logical_device in ["shutdown"]:
            return "0, 0,0,0,0,0,0,0,1, 0,0,"
        if logical_device in ["multiplier"]:
            return "0, 0,850,0,0,0,0,0,0, 0,0,"
        if logical_device in ["mode-change-delay"]:
            return "0, 0,1000,1000,1000,1000,0,0,0, 0,0,"
        if logical_device in ["mass-scale"]:
            return "0, 1,1,2,3,4,1,1,1, 0,0,"
        if logical_device in ["mass-range"]:
            return "0, 200.00,200.00,200.00,200.00,200.00,200.00,200.00,200.00, 0,0,"
        if logical_device in ["mass"]:
            return "0, 5.50,49.00,5.50,5.50,5.50,5.50,5.50,20.00, 0,0,"
        if logical_device in ["focus"]:
            return "0, -90,-90,-90,-90,-90,-90,-90,-90, 0,0,"
        if logical_device in ["enable-PIA"]:
            return "0, 1,1,1,1,1,1,1,0, 0,0,"
        if logical_device in ["emission-value"]:
            return "0, 20.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000,0.00000, 0,0,"
        if logical_device in ["emission-limit"]:
            return "0, 5000.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000, 0,0,"
        if logical_device in ["emission"]:
            return "0, 20.000,1000.000,1000.000,1000.000,1000.000,20.000,20.000,2700.000, 0,0,"
        if logical_device in ["electron-energy", "electron-energy-DAC"]:
            return "0, 70.0,70.0,70.0,70.0,4.0,4.0,4.0,135.0, 0,0,"
        if logical_device in ["display-error", "display-line"]:
            return "0, ,,,,,,,, 0,0,"
        if logical_device in ["clock"]:
            return "0, 01/01/70 00:00:00,01/01/70 00:00:00,01/01/70 00:00:00,01/01/70 00:00:00,01/01/70 00:00:00,01/01/70 00:00:00,01/01/70 00:00:00,01/01/70 00:00:00, 0,0,"
        if logical_device in ["cage"]:
            return "0, 0.0,3.0,0.0,0.0,0.0,0.0,5.0,-5.0, 0,0,"
        if logical_device in ["beep"]:
            return "0, 200,0,0,0,0,0,0,0, 0,0,"
        if logical_device in ["RGA-SIMS"]:
            return "0, 200,0,0,0,0,0,0,0, 0,0,"
        if logical_device in ["P5V12"]:
            return "0, 1480400.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000, 0,0,"
        if logical_device in ["N10V24"]:
            return "0, 48050.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000, 0,0,"
        if logical_device in ["0V"]:
            return "0, 1003100.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000, 0,0,"

        return "0, 0,0,0,0,0,0,0,0, 0,0,"
    
    @conditional_reply("connected")
    def rbuf(self):
        return ""  # OK
    
    @has_log
    def handle_error(self, request, error):
        err = "An error occurred at request {}: {}".format(str(request), str(error))
        print(err)
        self.log.error(err)
        return str(err)
