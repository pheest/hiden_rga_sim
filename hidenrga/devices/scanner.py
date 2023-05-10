class ScannerRow:
    def __init__(self):
        self._start = 2
        self._stop = 50
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
    def __init__(self, scan_output):
        self._rows = [ScannerRow()]
        self._current_row = 0
        self._scan_input = "Faraday"
        self._scan_output = scan_output
        self._report = 5
        
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
        return self._rows[0].start
        
    @property
    def current_row_start(self):
        return self._rows[self.current_row].start
        
    @current_row_start.setter
    def current_row_start(self, start):
        self._rows[self.current_row].start = start
        
    @property
    def stop(self):
        return self._rows[-1].stop
        
    @property
    def current_row_stop(self):
        return self._rows[self.current_row].stop
        
    @current_row_stop.setter
    def current_row_stop(self, stop):
        self._rows[self.current_row].stop = stop
        
    @property
    def current_row_step(self):
        return self._rows[self.current_row].step
        
    @current_row_step.setter
    def current_row_step(self, step):
        self._rows[self.current_row].step = step

    @property
    def scan_input(self):
        return self._scan_input
            
    @scan_input.setter
    def scan_input(self, input):
        self._scan_input = input

    @property
    def scan_output(self):
        return self._scan_output
            
    @scan_output.setter
    def scan_output(self, output):
        self._scan_output = output
        
    @property
    def report(self):
        return self._report
            
    @report.setter
    def report(self, report):
        self._report = report
