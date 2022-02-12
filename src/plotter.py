'''!@file       plotter.py
    The main code to run on the PC to run and plot a step response on
    a motor. Includes functionality to set the setpoint and controller gain.
    The data is exchanged with the microcontroller over serial.
    @author     Tori Bornino
    @author     Jackson McLaughlin
    @author     Zach Stednitz
    @date       January 27, 2022
'''

from matplotlib import pyplot
import serial
import time


_PPR = 256*4*16
_set_point = 360 # deg

# Open serial port with the Nucleo
_port = "COM3"

with serial.Serial(_port, 115200, timeout=1) as ser_port:
    # Reset the Nucleo and start its program
    ser_port.write(b'\x03')
    time.sleep(1)
    ser_port.write(b'\x02')
    time.sleep(1)
    ser_port.write(b'\x04')
    # Receive data from the Nucleo and process it into 2 lists
#     _xs = []
    voltages = []
    while True:
        line = ser_port.readline()
        print(line.decode('utf-8'), end='')
        if line[:4] == b'Done':
            break
        try:
            voltage = float(line.strip())
        except (ValueError, IndexError):
            continue
        voltages.append(voltage)
        
# Plot step response
times = range(2000)
pyplot.plot(times, voltages)
# Plot line for setpoint
# _t_max = _xs[-1]
# _set_point_ticks = _set_point * _PPR / 360
# pyplot.plot([0, _t_max], [_set_point_ticks, _set_point_ticks], 'r--')
pyplot.xlabel("time [ms]")
pyplot.ylabel("voltage [V]")
pyplot.show()