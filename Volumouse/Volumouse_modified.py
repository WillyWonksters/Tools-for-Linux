#!/usr/bin/env python
#-*-coding:utf-8-*-
# Trust in Pzim !
# python3-xlib package must be installed to run this script :
#sudo apt-get install python3-xlib
#or sudo apt-get install python-xlib

#import os
from subprocess import call
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

Screen_resolution = (2560,1440) # write here your screen resolution

Bottom_area = 50 # write here the number of pixels at the bottom of your screen that will represent the activation region.

# Let's set up the commands
def volume_up():
    
    call("amixer set Master 3%+",shell=True)


def volume_down():
    
    call("amixer set Master 3%-",shell=True)


record_dpy = display.Display()

ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.MotionNotify),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])

def record_callback(reply):

    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
        
        if event.type == X.ButtonPress:
            print (event.detail, event.root_x, event.root_y)
            
            #This has been altered from Pzim's orignal to ignore the x component, so that it is activated across the entire bottom of the screen
            if event.root_y > Screen_resolution[1] - Bottom_area:

               print ("Bottom area detected")

               if event.detail is 4 : # event.detail 4 means wheel up event
                  print ("volume up!") 
                  volume_up() 

               if event.detail is 5 : # event.detail 5 means wheel down event
                  print ("volume down!") 
                  volume_down() 
                                   
            
        elif event.type == X.ButtonRelease:

            print  (event.detail, event.root_x, event.root_y)
            
        elif event.type == X.MotionNotify:

            print (event.root_x, event.root_y)
            

record_dpy.record_enable_context(ctx, record_callback)
