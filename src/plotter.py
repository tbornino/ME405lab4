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

## Serial port used to communicate with the Nucleo
port = "COM3"

with serial.Serial(port, 115200, timeout=1) as ser_port:
    # Reset the Nucleo and start its program
    ser_port.write(b'\x03')
    time.sleep(1)
    ser_port.write(b'\x02')
    time.sleep(1)
    ser_port.write(b'\x04')
    ## List to store voltage data in
    voltages = []
    while True:
        ## Line of data from serial port
        line = ser_port.readline()
        # Echo serial received so we can see what is transmitted
        print(line.decode('utf-8'), end='')
        if line[:4] == b'Done':
            break
        try:
            ## Individual voltage reading
            voltage = float(line.strip())
        except (ValueError, IndexError):
            continue
        voltages.append(voltage)
        
# Plot step response
## List of times from 0 to 1999 ms
times = range(2000)
pyplot.plot(times, voltages)
pyplot.xlabel("Time [ms]")
pyplot.ylabel("Voltage [V]")
pyplot.show()