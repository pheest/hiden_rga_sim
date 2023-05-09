# -*- coding: utf-8 -*-
# *********************************************************************
# lewis - a library for creating hardware device simulators
# Copyright (C) 2016-2021 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************

from lewis.adapters.stream import Cmd, StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply
from lewis.core.logging import has_log


class HidenRGAStreamInterface(StreamInterface):
    """
    TCP-stream based Hiden RGA interface
    """
    
    commands = {
        CmdBuilder("get_name").escape("pget name ").build(),
        CmdBuilder("get_id").escape("pget ID ").build(),
        CmdBuilder("get_release").escape("pget release ").build(),
        CmdBuilder("get_configurationid").escape("pid# configuration ").build(),
        CmdBuilder("get_configurationid").escape("pget configuration ").build(),
        CmdBuilder("reset").escape("sdel all").build(),
        CmdBuilder("set_out").escape("sout").string().build(),
        CmdBuilder("set_err").escape("serr").string().build(),
        CmdBuilder("set_terse").escape("pset terse ").int().build(),
        CmdBuilder("sjob_sdel_all").escape("sjob sdel all").build(),
        CmdBuilder("sjob_lset").escape("sjob lset").string().build(),
        CmdBuilder("sjob_quit").escape("sjob quit").build(),
        CmdBuilder("sjob_lini").escape("sjob lini ").string().build(),
        CmdBuilder("lput").escape("lput ").string().float().escape(" ").float().build(),
        CmdBuilder("sjob_lput").escape("sjob lput ").string().float().escape(" ").float().build(),
        CmdBuilder("sjob_lget").escape("sjob lget ").string().build(),
        CmdBuilder("sjob_save").escape("sjob save ").string().build(),
        CmdBuilder("stat_job").escape("stat ").int().build(),
        CmdBuilder("stat_task").escape("stat task ").int().build(),
        CmdBuilder("lget_device").escape("lget ").string().build(),
        CmdBuilder("data_on").escape("data ").escape("on").build(),
        CmdBuilder("data_all").escape("data ").escape("all").build(),
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
        CmdBuilder("sset_mode").escape("lset mode ").int().build(),
        CmdBuilder("tdel_all").escape("tdel all").build(),
        CmdBuilder("quit").escape("quit").build(),
        CmdBuilder("sset_state_Abort").escape("sset state Abort:").build(),
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
    def get_id(self):
        return self.device.id
        
    @conditional_reply("connected")
    def get_release(self):
        return self.device.release

    @conditional_reply("connected")
    def get_configurationid(self):
        return 1

    @conditional_reply("connected")
    def get_configuration(self):
        return ""

    @conditional_reply("connected")
    def reset(self):
        self.device.reset()
        
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
        return "task 1, job 1," # Task <task#>, job <job#>,
        
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
        #if device == "cage":
            #self.device.cage = val1
        #if device == "F1":
            #self.device.F1 = val1
        #if device == "F2":
            #self.device.F2 = val1
        #if device == "delta-m":
            #self.device.delta-m = val1
        if device == "electron-energy":
            self.device.electron_energy = val1
        if device == "emission":
            self.device.emission = val1
        #if device = "focus":
            #self.device.focus = val1
        #if device = "mass":
            #self.device.mass = val1
        #if device = "mode-change-delay":
            #self.device.mode-change-delay = val1
        #if device = "multiplier":
            #self.device.multiplier = val1
        #if device = "resolution":
            #self.device.resolution = val1
       
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
    def lget_device(self, devID):
        retval = "0"
        if devID == 'emok' and self.device.emok:
            retval = "1"
        if devID == 'filok' and self.device.filok:
            retval = "1"
        if devID == 'ptrip' and self.device.ptrip:
            retval = "1"
        if devID == 'overtemp' and self.device.overtemp:
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
            self.device.dwell = int(dwell[:-1])
        else:
            self.device.dwell = int(dwell)
        self.device.dwellmode = dwellmode
        return ""  # OK
    
    @conditional_reply("connected")
    def sset_settle(self, settle):
        # Either e.g. 100 (time in ms) or eg 100% (percent of default value)
        settlemode = settle[len(settle)-1]=='%'
        if settlemode:
            self.device.settle = int(settle[:-1])
        else:
            self.device.settle = int(settle)
        self.device.settlemode = settlemode
        return ""  # OK
        
    def smax_interval(self):
        return 3600
    
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
        """Returns the current data string."""
        return ""  # OK
    
    @conditional_reply("connected")
    def data_all(self):
        """Returns the current data string."""
        return self.device.data(True)
    
    @conditional_reply("connected")
    def data(self):
        """Returns the current data string."""
        return self.device.data(False)
    
    @conditional_reply("connected")
    def pset_points(self, points):
        self.device.points = points
        return ""  # OK

    @conditional_reply("connected")
    def quit(self):
        return ""  # OK
        
        
    @conditional_reply("connected")
    def sset_state_Abort(self):
        if self.device.stat:
            self.device.stop()
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
        if logical_device == "mass":
            return self.device.max_mass
        if logical_device == "Faraday_range":
            return 1E-5
        return 0
    
    @conditional_reply("connected")
    def lres(self, logical_device):
        return 0.001
        
    @conditional_reply("connected")
    def lid_hash(self, logical_device):
        if logical_device == "state":
            return self.device.scan_table.index(logical_device)
            
        if logical_device not in self.device.logical_all:
            self.log.error("device not found")
            return 0
        return self.device.logical_all.index(logical_device)
    
    @conditional_reply("connected")
    def lid_dollar(self, logical_device):
        if logical_device == "all":
            return ' '.join(self.device.logical_all)
        if logical_device == "groups":
            return ' '.join(self.device.logical_groups)
        if logical_device == "rangedev":
            return ' '.join(self.device.logical_rangedev)
        if logical_device == "control":
            return ' '.join(self.device.logical_control)
        if logical_device == "degassing":
            return ""
        if logical_device == "environment":
            return ' '.join(self.device.logical_environment)
        if logical_device == "global":
            return ' '.join(self.device.logical_global)
        if logical_device == "input":
            return ' '.join(self.device.logical_input)
        if logical_device == "map":
            return ' '.join(self.device.logical_map)
        if logical_device == "measurement":
            return ' '.join(self.device.logical_measurement)
        if logical_device == "mode":
            return ' '.join(self.device.logical_mode)
        if logical_device == "others":
            return ' '.join(self.device.logical_others)
        if logical_device == "output":
            return ' '.join(self.device.logical_output)
        if logical_device == "quad":
            return ' '.join(self.device.logical_quad)
        if logical_device == "switched":
            return ' '.join(self.device.logical_switched)
        if logical_device == "total/partial":
            return ' '.join(self.device.logical_total_partial)
        return ""
    
    @conditional_reply("connected")
    def ltyp(self, logical_device):
        if logical_device == "quad":
            return "tune-group"
        if logical_device == "groups":
            return ' '.join(self.device.logical_groups)
        if logical_device == "rangedev":
            return ' '.join(self.device.logical_rangedev)
        return "group"
        
    @conditional_reply("connected")
    def luse(self, logical_index):
        logical_device = "unknown"
        if logical_index < len(self.device.logical_all):
            logical_device = self.device.logical_all[logical_index]
        self.log.info("logical device " + logical_device)
        return logical_device
    
    @conditional_reply("connected")
    def rerr(self):
        return ""  # OK
    
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
        return "1,5.50,5.50,5.50,5.50,5.50,5.50,5.50,5.50, 0.000000, 1.000000,"
        return ""
    
    @conditional_reply("connected")
    def rbuf(self):
        return ""  # OK
    
    @has_log
    def handle_error(self, request, error):
        err = "An error occurred at request {}: {}".format(str(request), str(error))
        print(err)
        self.log.info(err)
        return str(err)
