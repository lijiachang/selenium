
import wmi

wmiInterface = wmi.WMI()

process_info = {}
while True:  # Change the looping condition
    for process in wmiInterface.Win32_Process(name="services.exe"):
        id = process.ProcessID
        for p in wmiInterface.Win32_PerfRawData_PerfProc_Process(IDProcess=id):
            n1, d1 = long(p.PercentProcessorTime), long(p.Timestamp_Sys100NS)
            n0, d0 = process_info.get(id, (0, 0))
            try:
                percent_processor_time = (float(n1 - n0) / float(d1 - d0)) * 100.0
            except ZeroDivisionError:
                percent_processor_time = 0.0
            process_info[id] = (n1, d1)
            print id, process.Caption, str(percent_processor_time)