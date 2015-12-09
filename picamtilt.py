#!/usr/bin/python

# Copyright (C) 2015 RealVNC Limited. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#   1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 
#   2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 
#   3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.

# picamtilt - A UI for controlling a pan-tilt unit with a mounted Raspberry Pi
# camera, overlayed with the camera preview image.

import time, random
from Tkinter import *
from Adafruit_PWM_Servo_Driver import PWM
import picamera

# Title text
title = "RealVNC\nRaspberry Pi\nCamera control"

# Starting position
# Position in each direction is specified in the range 0...1
# where 0,0 is top/left and 1,1 is bottom/right.
x = 0.5
y = 0.5

# Radius of marker circle
r = 30

# Amount to move for Up/Down/Left/Right keypresses
kd = 0.05

canvas = 0
width = 0
height = 0
marker = 0
demo = False

# Set PWM output
def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  pulseLength /= 4096                     # 12 bits of resolution
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, int(pulse))

# Move servos immediately to a specified x, y position
def moveTo(x, y):
  sx = 2600 - (x*2000)
  sy = 600 + (y*1200)
  setServoPulse(0, float(sx / 1000.0))
  setServoPulse(1, float(sy / 1000.0))
  ax = x * width
  ay = y * height
  canvas.coords(marker,ax-r,ay-r,ax+r,ay+r)

# Move servos from the current position to a new position given by tx,ty
# in the given number of steps.
def slewTo(tx, ty, steps):
  global x
  global y
  dx = (tx - x) / float(steps)
  dy = (ty - y) / float(steps)
  for s in range(0,steps,1):
    x += dx
    y += dy
    moveTo(x,y)
    root.update()

# Handle canvas resize
def resize(event):
    global width
    global height
    global marker
    width = root.winfo_width(); 
    height = root.winfo_height();

    canvas.delete(ALL)

    # Draw outline rectange
    canvas.create_rectangle(1,1,width-2,height-2,fill="white");

    ax = x * width
    ay = y * height
    marker = canvas.create_oval(ax-r,ay-r,ax+r,ay+r,fill="blue")

    # Draw centre lines
    canvas.create_line(90, height/2, width-120, height/2, 
                       dash=(20,20), width=3);
    canvas.create_line(width/2, 40, width/2, height-40, 
                       dash=(20,20), width=3);

    # Add some text
    canvas.create_text(width/2,20,text="UP", 
                       font=("sans-serif",20), fill="Red");
    canvas.create_text(width/2,height-20,text="DOWN",
                       font=("sans-serif",20), fill="Red");
    canvas.create_text(45,height/2,text="LEFT",
                       font=("sans-serif",20), fill="Red");
    canvas.create_text(width-60,height/2,text="RIGHT",
                       font=("sans-serif",20), fill="Red");

    canvas.create_text(140,height-65,text=title,
                       font=("sans-serif",25), fill="Black");

# Handle mouse click events
def click(event):
    global x
    global y
    global demo
    demo = False
    x = float(event.x) / width
    y = float(event.y) / height
    moveTo(x,y)

# Handle key events
def key(event):
    global x
    global y
    global demo
    if (event.keysym == "q"): root.quit()
    if (event.keysym == "Up"): y = y - kd
    if (event.keysym == "Down"): y = y + kd
    if (event.keysym == "Left"): x = x - kd
    if (event.keysym == "Right"): x = x + kd
    if (event.keysym == "space"): 
        x = 0.5
        y = 0.5
    if (x > 1): x = 1
    if (x < 0): x = 0
    if (y > 1): y = 1
    if (y < 0): y = 0
    if (event.keysym == "d"): 
      demo = True
      root.after(0, runDemo)
    else:
      demo = False
    moveTo(x,y)

# Move to the next random position in demo mode
def runDemo():
  if (demo):
    tx = random.randint(0,1000)/1000.0
    ty = random.randint(0,1000)/1000.0
    slewTo(tx,ty,100)
    root.after(2000, runDemo)



# Setup the window and canvas
root = Tk()
root.attributes('-fullscreen',True);
root.bind("<Button-1>", click);
root.bind_all("<KeyRelease>", key);
canvas = Canvas(root);
canvas.bind("<Configure>", resize)
canvas.pack(fill=BOTH, expand=YES);

# Setup the PWM
pwm = PWM(0x40)
pwm.setPWMFreq(60)

# Start the camera preview
cam = picamera.PiCamera()
cam.start_preview()
cam.preview_alpha = 192

# Move to starting position
moveTo(x,y);

# Enter main loop
root.mainloop()

# Cleanup
cam.stop_preview()
cam.close()
