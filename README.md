# picamtilt

A UI for controlling a pan-tilt unit with a mounted Raspberry Pi camera, 
overlayed with the camera preview image.

Written in Python, using Tkinter for the UI and the picamera Python module
to control the Raspberry Pi camera preview.

Run the program from the repo directory, via sudo:
```bash
$ sudo python picamtilt.py
```

The program creates a full-screen window, with cross-hairs and a blue circle 
showing the current camera position. The Raspberry Pi camera preview is shown 
full-screen with transparency, so the UI is superimposed on the camera image.

Controls are:
- Mouse click: moves the camera to specific point.
- Arrow keys: Moves the camera by fixed amount in that direction.
- Space: Move to the centre.
- d: Enters "demo mode", where the camera will move about randomly (any other key exits demo).
- q: Quits the program.

This was written to provide a demonstration of RealVNC's
[VNC Server for Raspberry Pi](https://www.realvnc.com/products/vnc/raspberrypi/) 
at the [PiWars](http://piwars.org/) event in December 2015.


The following instructions detail how to build the complete system:

## Hardware

### Parts required

- Official Raspberry Pi camera 
You could also use the PI NOIR camera if you want to do infra-red.

- [Pan+tilt unit](http://4tronix.co.uk/store/index.php?rt=product/product&keyword=tilt&category_id=0&product_id=435) with servos and camera mount, from 4tronix


- Long camera cable (30cm or more)
The standard cable supplied with the Raspberry Pi camera is too short when used
with the Pan+tilt unit.

- [PWM/servo hat](http://www.adafruit.com/products/2327) for Raspberry Pi, from Adafruit


- A Raspberry Pi
Any model except the Pi Zero (since it has no camera connector), but preferably 
one of the newer models (2B, B+ or A+) which are designed to fit HAT add-ons. 
According to Adafruit, the PWM hat can be made to fit onto an older Pi if longer 
headers are used.

- A suitable power supply for the Raspberry Pi.

- A suitable power supply for the servos (see powering the servos section).

### Assembly

Assemble everything, remembering to thread the camera cable through the slot in
the PWM hat and plugging this into the Pi before attaching the hat. Observe the
polarity of the servo connections (brown wire=gnd, red=+v, orange=signal), and 
plug the cable from the pan (rotate) servo into channel 0 and the tilt (up/down) 
servo into channel 1. Note that the hat can support a total of 16 servos, so 
there is plenty of room for adding extra functionality!

### Powering the servos

You should also use a separate power supply for the servos, since it is not 
recommended to power them off the same supply as the Pi. This [3 AA battery box](http://www.maplin.co.uk/p/3-aa-battery-box-yr61r) from Maplin is suitable.
Plus a [PP3 battery clip connector](http://www.maplin.co.uk/p/pp3-snap-battery-clip-hf28f), 
which can be wired to the screw terminals on the PWM hat (also observing the 
polarity!). Using standard alkaline AA batteries, this provides a 4.5v supply
to the servos.

### Case

A suitable case was 3D printed to house the Raspberry Pi and PWM hat, and 
allow the Pan+tilt unit to be mounted on top. The following case was used from
Thingiverse:
[Raspberry Pi B+ Case with Camera Hole "Valkyrie" by rgbextruder](http://www.thingiverse.com/thing:552193)

The top was modified by cutting out a hole in the corner to allow access to the
PWM outputs, and to allow the camera and power cables to enter. The STL file 
for the modified top is included in this repo as "case_top_cutout.stl", and is
licensed under the [Creative Commons - Attribution - Share Alike license](http://creativecommons.org/licenses/by-sa/3.0/)


## Software

- Install the python package for controlling the Pi camera
```bash
$ sudo apt-get install python-picamera
```

- Install the python Tkinter UI library: 
```bash
$ sudo apt-get install python-tk
```

- Follow the [Adafruit tutorial](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/) 
to setup the PWM hat and install the software.

- Clone this repo and copy in the required files from the Adafruit-Raspberry-Pi-Python-Code
installation directory, e.g. (assuming you installed it under your home directory):
```bash
$ git clone https://github.com/RealVNC/picamtilt.git
$ cd picamtilt
$ cp ~/Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver/Adafruit_PWM_Servo_Driver.* .
$ cp ~/Adafruit-Raspberry-Pi-Python-Code/Adafruit_I2C/Adafruit_I2C.* .
```

Copyright (C) 2015 RealVNC Limited. All rights reserved.
