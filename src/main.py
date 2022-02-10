"""!
@file main.py
    This file contains a program capable of running multiple tasks simultaneously
    using a real time scheduler. 

@author             Tori Bornino
@author             Jackson McLaughlin
@author             Zach Stednitz
@date               February 17, 2022

"""
import pyb
from pyb import ADC

#Create the queue
pin_reading_queue = task_share.Queue(h, 1000, thread_protect = True,
                                     overwrite = False, name = "Pin C0 Readings")

#create the pins and timer objects
pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
tim1 = pyb.Timer(1, freq = 1000, pin = pinC0)
adc = ADC(pin_reading_queue)

def interruptFCN(IRQ_src):
    pin_reading_queue.put(adc.read())
    print('interrupt')
interrupt = pyb.ExtInt(pinC0, mode=pyb.ExtInt.IRQ_FALLING,
                       pull=pyb.Pin.PULL_NONE, callback = interruptFCN)

if __name__ == "__main__":
    pass