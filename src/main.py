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
import micropython

micropython.alloc_emergency_exception_buf(100)
# State Variables for pin
_PIN_LOW = 0
_PIN_HIGH = 1
V_CC = 3.3
def interruptFCN(IRQ_src):
    '''!
    This interrupt method reads the ADC output for the voltage across the
    capacitor.
    
    @param IRQ_src The return location after ISR is complete.
    '''
    
#     print("interrupt")
#     try:
    pin_reading_queue.put(adc.read())
#         print_task.put('interrupt')
#     except TypeError:
#         print(adc.read(), 'TypeError')

        
# def step_responseFCN():
#     '''!
#     This generator toggles the pin state between high and low.
#     '''
#     state = _PIN_LOW
#     while True:
#         print('in SR')
#         if state == _PIN_LOW:
#             pinC1.high()
#             state = _PIN_HIGH
#         elif state == _PIN_HIGH:
#             pinC1.low()
#             state = _PIN_LOW
#         yield(state)

if __name__ == "__main__":
    #Create the queue
    pin_reading_queue = task_share.Queue('H', 2000, thread_protect = True,
                                         overwrite = False, name = "Pin C0 Readings")
# 
#     #create the pins and timer objects
    pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
    pinC1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    tim1 = pyb.Timer(1, freq = 1000)
#     
#     # initiate the task to toggle the pin between high and low
#     task_step = cotask.Task (step_responseFCN, name = 'Step Response', priority = 0, 
#                          period = 2000, profile = True, trace = False)
#     
#     # Initialize the ADC and ISR to run at timer frequency
    adc = ADC(pinC0)
    tim1.callback(interruptFCN)
    pinC1.high()
    while not pin_reading_queue.full():
        pass
    tim1.callback(None)
    while pin_reading_queue.any():
        print(pin_reading_queue.get() * V_CC / 4095)
    print("Done")
    pinC1.low()
    
    # Add toggle to task list and run garbage collector
#     cotask.task_list.append(task_step)
#     gc.collect ()
#     
#     while True:
# #         print('in main loop')
#         try:
#             cotask.task_list.pri_sched ()
#         except KeyboardInterrupt:
#             print('Keyboard interrupt')
#             break