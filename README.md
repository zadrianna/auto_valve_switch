# Automatic Valve Switch Program

This program uses the nidaqmx package to control opening and closing valves via a National Instruments DAQ device.
The program is capable of controlling individual valves, setting switch delays and running pre-programmed times switches.

**Be advised**: this was written by someone who has no idea what they're doing, so the quality of the program is questionable at best. You can do better than this.

- **Switch_program_1.0.py** utilises the Tk interface package for GUI construction and had no multi-threading implemented. Thus, the GUI freezes during long-running tasks
- **switch_program_2.0.py** uses the PyQT6 package for both GUI construction and multi-threading 



