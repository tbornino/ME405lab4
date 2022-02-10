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
import print_task
import task_share
import cotask
import gc

_PIN_LOW = 0
_PIN_HIGH = 1

def interruptFCN(IRQ_src):
    try:
        pin_reading_queue.put(adc.read())
        print_task.put('interrupt')
        print('Interrupted')
    except TypeError as terr:
        print(adc.read(), 'TypeError')
def step_responseFCN():
    state = _PIN_LOW
    while True:
        print('in SR')
        if state == _PIN_LOW:
            pinC1.high()
            state = _PIN_HIGH
        elif state == _PIN_HIGH:
            pinC1.low()
            state = _PIN_LOW
        yield(state)

if __name__ == "__main__":
    #Create the queue
    pin_reading_queue = task_share.Queue('H', 1000, thread_protect = True,
                                         overwrite = False, name = "Pin C0 Readings")

    #create the pins and timer objects
    pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
    pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    tim1 = pyb.Timer(1, freq = 1000)
    
    task_step = cotask.Task (step_responseFCN, name = 'Step Response', priority = 0, 
                         period = 2000, profile = True, trace = False)

    adc = ADC(pinC0)
    tim1.callback(interruptFCN)
    
    cotask.task_list.append(task_step)
    gc.collect ()
    
    while True:
#         print('in main loop')
        try:
            cotask.task_list.pri_sched ()
        except KeyboardInterrupt:
            print('Keyboard interrupt')
            break