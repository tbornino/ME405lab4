"""!
@file main.py
This file contains a program which runs a step response on an RC circuit and
takes data on the voltage every 1ms using an interrupt. This is then sent to
a PC over serial, so it can be plotted.

@author             Tori Bornino
@author             Jackson McLaughlin
@author             Zach Stednitz
@date               February 17, 2022

"""
import pyb
from pyb import ADC
import micropython
import task_share

micropython.alloc_emergency_exception_buf(100)

## Logic high voltage (max used for ADC)
V_CC = 3.3

def interruptFCN(IRQ_src):
    '''!
    This interrupt method reads the ADC output for the voltage across the
    capacitor.
    
    @param IRQ_src The return location after ISR is complete.
    '''
    pin_reading_queue.put(adc.read())

if __name__ == "__main__":
    ## The queue for ADC readings (2s long)
    pin_reading_queue = task_share.Queue('H', 2000, thread_protect = True,
                                         overwrite = False, name = "Pin C0 Readings")
    
    ## Pin C0, used to read voltage of RC circuit
    pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
    ## Pin C1, used as input to RC circuit (toggled for step response)
    pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    ## Timer to run interrupt on
    tim1 = pyb.Timer(1, freq = 1000)

    ## ADC used to measure voltage across RC circuit
    adc = ADC(pinC0)
    # Set ISR to run at timer frequency
    tim1.callback(interruptFCN)
    # Toggle pin high for step response
    pinC1.high()
    # Wait until the queue of values is full
    while not pin_reading_queue.full():
        pass
    # Disable the interrupt so we can print the data
    tim1.callback(None)
    # Print the data, converted to voltage values for plotting
    while pin_reading_queue.any():
        print(pin_reading_queue.get() * V_CC / 4095)
    # Print this so we know when to stop plotting
    print("Done")
    # Toggle pin low for next time
    pinC1.low()