# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:35:47 2023

@author: adriannazgraj
"""
import nidaqmx
import time

def generate_pulse(duration, voltage, start_time, enable_pulse):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan("Dev1/port0/line1")  # Modify channel name accordingly

        # Wait until the specified start time
        current_time = time.time()
        wait_time = start_time - current_time
        if wait_time > 0:
            time.sleep(wait_time)

        # Set the initial state of the pulse
        task.write(bool(enable_pulse))

        # Generate the pulse for the specified duration
        task.start()
        time.sleep(duration)
        task.stop()

# Example usage: generate a 5V pulse for 1 second, starting at a specific time,
# and turn the pulse on (True) or off (False)
duration = 1  # Duration of the pulse in seconds
voltage = 5  # Voltage level of the pulse in volts
start_time = time.time() + 4  # Start time in 10 seconds from the current time
enable_pulse = True  # True to turn the pulse on, False to turn it off

generate_pulse(duration, voltage, start_time, enable_pulse)

