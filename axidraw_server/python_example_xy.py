#!/usr/bin/env python
# -*- encoding: utf-8 -#-

'''
python_example_xy.py

Demonstrate use of axidraw module in "interactive" mode.

Run this demo by calling: python python_example_xy.py


(There is also a separate "plot" mode, which can be used for plotting an
SVG file, rather than moving to various points upon command.)


'''


'''
About this software:

The AxiDraw writing and drawing machine is a product of Evil Mad Scientist
Laboratories. https://axidraw.com   https://shop.evilmadscientist.com

This open source software is written and maintained by Evil Mad Scientist
to support AxiDraw users across a wide range of applications. Please help
support Evil Mad Scientist and open source software development by purchasing
genuine AxiDraw hardware.

AxiDraw software development is hosted at https://github.com/evil-mad/axidraw

Additional AxiDraw documentation is available at http://axidraw.com/docs

AxiDraw owners may request technical support for this software through our 
github issues page, support forums, or by contacting us directly at:
https://shop.evilmadscientist.com/contact



Copyright 2018 Windell H. Oskay, Evil Mad Scientist Laboratories

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''






'''

Interactive mode is a mode of use, designed for plotting individual motion
segments upon request. It is a complement to the usual plotting modes, which
take an SVG document as input.

So long as the AxiDraw is started in the home corner, moves are limit checked,
and constrained to be within the safe travel range of the AxiDraw.



Recommended usage:

ad = axidraw.AxiDraw() # Initialize class
ad.interactive()            # Enter interactive mode

[Optional: Apply custom settings]

ad.connect()                # Open serial port to AxiDraw 

[One or more motion commands]
[Optional: Update settings, followed by calling update().]

ad.disconnect()             # Close connection to AxiDraw


The motion commands are as follows:

goto(x,y)    # Absolute XY move to new location
moveto(x,y)  # Absolute XY pen-up move. Lift pen before moving, if it is down.
lineto(x,y)  # Absolute XY pen-down move. Lower pen before moving, if it is up.

go(x,y)      # XY relative move.
move(x,y)    # XY relative pen-up move. Lift pen before moving, if it is down.
line(x,y)    # XY relative pen-down move. Lower pen before moving, if it is up.

penup()      # lift pen
pendown()    # lower pen


Utility commands:

interactive()   # Enter interactive mode
connect()       # Open serial connection to AxiDraw. Returns True if connected successfully.
update()        # Apply changes to options
disable()       # Disable XY motors, for example to manually move carriage to home position. 
disconnect()    # Terminate serial session to AxiDraw. (Required.)




The available options are as follows:

options.speed_pendown   # Range: 1-110 (percent). 
options.speed_penup     # Range: 1-110 (percent). 
options.accel           # Range: 1-100 (percent). 
options.pen_pos_down    # Range: 0-100 (percent). 
options.pen_pos_up      # Range: 0-100 (percent).
options.pen_rate_lower  # Range: 1-100 (percent).
options.pen_rate_raise  # Range: 1-100 (percent).
options.pen_delay_down  # Range: -500 - 500 (ms).
options.pen_delay_up    # Range: -500 - 500 (ms).
options.const_speed     # True or False. Default: False
options.units	        # Range: 0-1.  0: Inches (default), 1: cm
options.model           # Range: 1-3.   1: AxiDraw V2 or V3 ( Default)
                        #               2: AxiDraw V3/A3
                        #               3: AxiDraw V3 XLX
options.port            # String: Port name or USB nickname
options.port_config     # Range: 0-1.   0: Plot to first unit found, unless port specified. (Default)
                        #               1: Plot to first unit found

One or more options can be set after the interactive() call, and before connect() 
for example as:

ad.options.speed_pendown = 75



All options except port and port_config can be changed after connect(). However,
you must call update() after changing the options and before calling any
additional motion commands.


'''

import sys

from pyaxidraw import axidraw

ad = axidraw.AxiDraw() # Initialize class

ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw 


def left():
	ad.go(-1, 0)

def d(num):
	ad.options.pen_pos_down=num
	ad.update()
	ad.penup()
	ad.pendown()

def u(num):
	ad.options.pen_pos_up=num
	ad.update()
	ad.pendown()
	ad.penup()

def right():
	ad.go(1, 0)

def down():
	ad.go(0,1)

def up():
	ad.go(0, -1)

def wayleft():
	ad.go(-8,0)

def wayright():
	ad.go(8,0)