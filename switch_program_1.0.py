# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:35:29 2023

@author: adriannazgraj
"""

## for simplicity's sake: device off = valve closed

##probably important: if the program runs over midnight, it might break :) 

import tkinter as tk
from tkinter import messagebox
import nidaqmx
import time
import schedule
import datetime as dt

#%%
def create_daq_task(channel):
    # Create a DAQ task
    task = nidaqmx.Task()
    task.do_channels.add_do_chan(channel)
    return task

def open_valve(task_on, task_off, delay_entry, status_label): #opens a specified valve
    # Get the delay value from the entry field
    delay = delay_entry.get()
    
    try:
        delay = float(delay)
        if delay < 0:
            raise ValueError()
        
        # Turn on the device
        task_on.write(True)  # Set line1 voltage level to 5V
        task_off.write(False)  # Set line2 voltage level to 0V
        
        
        # Update status label
        status_label.config(text="OPEN", fg="green")
        
    except ValueError:
        messagebox.showerror("Invalid Delay", "Invalid delay value! Please enter a numeric non-negative value.")

def close_valve(task_on, task_off, delay_entry, status_label): #closes a specified valve
    # Get the delay value from the entry field
    delay = delay_entry.get()
    
    try:
        delay = float(delay)
        if delay < 0:
            raise ValueError()
        
        # Turn off the device
        task_on.write(False)  # Set line1 voltage level to 0V
        task_off.write(True)  # Set line2 voltage level to 5V
        
        
        # Update status label
        status_label.config(text="CLOSED", fg="red")
        
    
    except ValueError:
        messagebox.showerror("Invalid Delay", "Invalid delay value! Please enter a numeric non-negative value.")
        
        
def in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2): #opens valve 1 and closes valve 2
    delay = delay_entry.get()
    
    open_valve(task_on_1, task_off_1, delay_entry, status_label_1)
    close_valve(task_on_2, task_off_2, delay_entry, status_label_2)
    

def in_drug_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2): #opens valve 1 and closes valve 2
    delay = delay_entry.get()
    
    open_valve(task_on_2, task_off_2, delay_entry, status_label_2)
    close_valve(task_on_1, task_off_1, delay_entry, status_label_1)

def out_reg_acsf(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5): #opens valve 3 and closes valves 4 and 5
    
    open_valve(task_on_3, task_off_3, delay_entry, status_label_3)
    close_valve(task_on_4, task_off_4, delay_entry, status_label_4)
    close_valve(task_on_5, task_off_5, delay_entry, status_label_5)

def out_drug_acsf(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5): #opens valve 4 and closes 3 and 5
    
    close_valve(task_on_3, task_off_3, delay_entry, status_label_3)
    open_valve(task_on_4, task_off_4, delay_entry, status_label_4)
    close_valve(task_on_5, task_off_5, delay_entry, status_label_5)
    
def out_waste(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5): #opens valve 5 and closes 3 and 4
    
    close_valve(task_on_3, task_off_3, delay_entry, status_label_3)
    close_valve(task_on_4, task_off_4, delay_entry, status_label_4)
    open_valve(task_on_5, task_off_5, delay_entry, status_label_5)
    
        
def job_40bl_15ind(task_on_1, task_off_1, task_on_2, task_off_2, task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_3, status_label_4, status_label_5): 
#job: induction protocol with 40 min baseline and 15 min induction and reg switch after that
   #wait 40 min for baseline
   # time.sleep(2400)
   time.sleep(10) #test
   
   #switch to drug acsf
   in_drug_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
   out_waste(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)
   window.update_idletasks()
   #wait for 6 min for the drug acsf to come back around
   #time.sleep(360)
   time.sleep(2) #test
   
   #switch output to drug ascf tube
   out_drug_acsf(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)
   window.update_idletasks()
   #wait 9 min for the rest of the induction
   # time.sleep(540)
   time.sleep(5) #test
   
   #switch to regular acsf 
   in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
   out_waste(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)
   window.update_idletasks()
   #wait 6 min for ascf to circulate again
   #time.sleep(360)
   time.sleep(2) #test
   
   #switch to reg acsf out
   out_reg_acsf(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)
   window.update_idletasks()
  
   
def job_w_clean(task_on_1, task_off_1, task_on_2, task_off_2, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_5):
    #clean out regular ascf tubing
    in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
    out_waste(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)
    window.update_idletasks()
    #wait for the water to all flow through
    time.sleep(2)
    #switch to other tube
    in_drug_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
    window.update_idletasks()
    #wait
    time.sleep(2)
    #switch back to default
    in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
    window.update_idletasks()
    
    
def job_we_clean(task_on_1, task_off_1, task_on_2, task_off_2, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_5):
     #clean out regular ascf tubing 
     #ETHANOL
     in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
     out_waste(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)
     window.update_idletasks()
     #wait for the water to all flow through
     time.sleep(2)
     #switch to other tube
     in_drug_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
     window.update_idletasks()
     #wait
     time.sleep(2)
     #switch back to default
     # WATER
     in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
     window.update_idletasks()   
     time.sleep(2)
     #switch to other tube
     in_drug_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
     window.update_idletasks()
     #wait
     time.sleep(2)
     #switch back to default
     in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)
     window.update_idletasks()  
     
def schedule_job():
    desired_time_str = time_entry.get()
    try:
        desired_time = dt.datetime.strptime(desired_time_str, "%H:%M:%S").time()
    except ValueError:
        schedule_label.config(text="Invalid time format. Use HH:MM:SS.", fg="red")
        return

    current_time = dt.datetime.now().time()
    desired_datetime = dt.datetime.combine(dt.date.today(), desired_time)

    while current_time < desired_time:
        time.sleep(1)
        current_time = dt.datetime.now().time()
    print("executing scheduled task now")   
    job_40bl_15ind(task_on_1, task_off_1, task_on_2, task_off_2, task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_3, status_label_4, status_label_5)  # Execute the task at the desired time
    
    
    # #get the current time
    # now = dt.datetime.now()
    
    # target_time = time_entry.get()
    
    # try:
    #     # Convert the target time string to a datetime object
    #     target_time = dt.datetime.strptime(target_time, "%H:%M:%S").time()

    #     # Set the target time with the date from the current time
    #     target_datetime = dt.datetime(
    #         year=now.year, month=now.month, day=now.day,
    #         hour=target_time.hour, minute=target_time.minute, second=target_time.second
    #         )
        

    #     # Check if the current time is past the target time, if so, schedule for the next day
    #     if now >= target_datetime:
    #         target_datetime += dt.timedelta(days=1)
            

    #     # Calculate the delay until the target time
    #     # schedule_delay = (target_datetime - now).total_seconds()


    #     # Schedule function_A to run after the delay
    #     schedule.every().day.at(target_datetime.strftime("%H:%M:%S")).do(job_40bl_15ind(task_on_1, task_off_1, task_on_2, task_off_2, task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_3, status_label_4, status_label_5))

    #     # Run the scheduled jobs
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)

    # except ValueError:
    #     print("Invalid target time format. Please use HH:MM:SS.")



   
def job_quit(task_on_1, task_off_1, task_on_2, task_off_2, task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_3, status_label_4, status_label_5):
    
    open_valve(task_on_1, task_off_1, delay_entry, status_label_1)
    open_valve(task_on_5, task_off_5, delay_entry, status_label_5)
    close_valve(task_on_2, task_off_2, delay_entry, status_label_2)
    close_valve(task_on_3, task_off_3, delay_entry, status_label_3)
    close_valve(task_on_4, task_off_4, delay_entry, status_label_4)
    window.update_idletasks()
    
    time.sleep(2)
    
    window.destroy()
    

    

# Create DAQ tasks for line1 and line2 of Valve 1
task_on_1 = create_daq_task("Dev1/port0/line1")  # Task for turning on the device
task_off_1 = create_daq_task("Dev1/port0/line2")  # Task for turning off the device

#Create DAQ tasks for line1 and line2 of Valve 2
task_on_2 = create_daq_task("Dev1/port0/line3")  # Task for turning on the device
task_off_2 = create_daq_task("Dev1/port0/line4")  # Task for turning off the device

# Create DAQ tasks for line1 and line2 of Valve 3
task_on_3 = create_daq_task("Dev1/port0/line5")  # Task for turning on the device
task_off_3 = create_daq_task("Dev1/port0/line6")  # Task for turning off the device

# Create DAQ tasks for line1 and line2 of Valve 4
task_on_4 = create_daq_task("Dev1/port0/line7")  # Task for turning on the device
task_off_4 = create_daq_task("Dev1/port1/line0")  # Task for turning off the device

# Create DAQ tasks for line1 and line2 of Valve 5
task_on_5 = create_daq_task("Dev1/port1/line1")  # Task for turning on the device
task_off_5 = create_daq_task("Dev1/port1/line2")  # Task for turning off the device


#%% NEW GUI
window = tk.Tk() #create main window
window.title("Switch GUI")
window.config(bg="lightgrey")

#make frames
status_frame = tk.Frame(window, bg="grey", borderwidth=2)
status_frame.grid(row=0, column=0, padx=1, pady=2, sticky="w")

flow_frame = tk.Frame(window, bg="grey", borderwidth=2)
flow_frame.grid(row=1, column=0, padx=1, pady=2, sticky="w")

valve_frame = tk.Frame(window, bg="grey", borderwidth=2)
valve_frame.grid(row=2, column=0, padx=1, pady=2, sticky="w")

job_frame = tk.Frame(window, bg="grey", borderwidth=2)
job_frame.grid(row=3, column=0, padx=1, pady=2, sticky="nsw")

quit_frame = tk.Frame(window, bg="grey", borderwidth=2)
quit_frame.grid(row=3, column=1, padx=1, pady=2, sticky="sw")



## flow setting frame
#make buttons for in and outflows
r_acsf_button = tk.Button(flow_frame, text="Reg. ACSF IN", width=10, bg="#8e9e8f", command=lambda: in_reg_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)) #command for turning on valve 1 and off valve 2
r_acsf_button.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

d_acsf_button = tk.Button(flow_frame, text="Drug ACSF IN", width=10, bg="#8e9e8f", command=lambda: in_drug_acsf(task_on_1, task_off_1, task_on_2, task_off_2, delay_entry, status_label_1, status_label_2)) # command for turning on valve 2 and offf valve 1
d_acsf_button.grid(row=0, column=1, padx=5, pady=3, ipadx=10)

outreg_button = tk.Button(flow_frame, text="OUT Reg. ACSF", width=10, bg="#b59696", command=lambda: out_reg_acsf(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)) #+ command for turning on valve 3 and off 4 and 5
outreg_button.grid(row=0, column=2, padx=5, pady=3, ipadx=10)

outdrug_button = tk.Button(flow_frame, text="OUT Drug ACSF", width=10, bg="#b59696", command=lambda: out_drug_acsf(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)) #+ command for turning on valve 4 and off 3 and 5
outdrug_button.grid(row=0, column=3, padx=5, pady=3, ipadx=10)

waste_button = tk.Button(flow_frame, text="OUT Waste", width=10, bg="#b59696", command=lambda: out_waste(task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry, status_label_3, status_label_4, status_label_5)) #+ command for turning on valve 5 and off 3 and 4 
waste_button.grid(row=0, column=4, padx=5, pady=3, ipadx=10)


 ## valve frame
 #valve 1
tk.Label(valve_frame, text="Valve 1", width=15).grid(row=0, column=0)
status_label_1 = tk.Label(valve_frame, text="CLOSED", fg="red")
status_label_1.grid(row=1, column=0)
valve1_open = tk.Button(valve_frame, text="O", command=lambda: open_valve(task_on_1, task_off_1, delay_entry, status_label_1)).grid(row=2, column=0, padx=5, pady=5)
valve1_close = tk.Button(valve_frame, text="C",  command=lambda: close_valve(task_on_1, task_off_1, delay_entry, status_label_1)).grid(row=3, column=0, padx=5, pady=5)

#valve 2
tk.Label(valve_frame, text="Valve 2", width=15).grid(row=0, column=1)
status_label_2 = tk.Label(valve_frame, text="CLOSED", fg="red")
status_label_2.grid(row=1, column=1)
valve2_open = tk.Button(valve_frame, text="O", command=lambda: open_valve(task_on_2, task_off_2, delay_entry, status_label_2)).grid(row=2, column=1, padx=5, pady=5)
valve2_close = tk.Button(valve_frame, text="C", command=lambda: close_valve(task_on_2, task_off_2, delay_entry, status_label_2)).grid(row=3, column=1, padx=5, pady=5)

#valve 3
tk.Label(valve_frame, text="Valve 3", width=15).grid(row=0, column=2)
status_label_3 = tk.Label(valve_frame, text="CLOSED", fg="red")
status_label_3.grid(row=1, column=2)
valve3_open = tk.Button(valve_frame, text="O", command=lambda: open_valve(task_on_3, task_off_3, delay_entry, status_label_3)).grid(row=2, column=2, padx=5, pady=5)
valve3_close = tk.Button(valve_frame, text="C", command=lambda: close_valve(task_on_3, task_off_3, delay_entry, status_label_3)).grid(row=3, column=2, padx=5, pady=5)

#valve 4
tk.Label(valve_frame, text="Valve 4", width=15).grid(row=0, column=3)
status_label_4 = tk.Label(valve_frame, text="CLOSED", fg="red")
status_label_4.grid(row=1, column=3)
valve4_open = tk.Button(valve_frame, text="O", command=lambda: open_valve(task_on_4, task_off_4, delay_entry, status_label_4)).grid(row=2, column=3, padx=5, pady=5)
valve4_close = tk.Button(valve_frame, text="C", command=lambda: close_valve(task_on_4, task_off_4, delay_entry, status_label_4)).grid(row=3, column=3, padx=5, pady=5)

#valve 5
tk.Label(valve_frame, text="Valve 5", width=15).grid(row=0, column=4)
status_label_5 = tk.Label(valve_frame, text="CLOSED", fg="red")
status_label_5.grid(row=1, column=4)
valve5_open = tk.Button(valve_frame, text="O", command=lambda: open_valve(task_on_5, task_off_5, delay_entry, status_label_5)).grid(row=2, column=4, padx=5, pady=5)
valve5_close = tk.Button(valve_frame, text="C", command=lambda: close_valve(task_on_5, task_off_5, delay_entry, status_label_5)).grid(row=3, column=4, padx=5, pady=5)

## jobs frame
tk.Label(job_frame, text="Preset Jobs:").grid(row=0, padx=5, pady=5)

tk.Label(job_frame, text="INDUCTION: 40m BL, 15m IND").grid(row=1, column=0, padx=15, pady=5)
tk.Button(job_frame, text="START", command=lambda: job_40bl_15ind(task_on_1, task_off_1, task_on_2, task_off_2, task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_3, status_label_4, status_label_5)).grid(row=1, column=1, padx=5, pady=5) #task for switching valves w/ appropraite delays
tk.Button(job_frame, text="SCHEDULE", command=lambda: schedule_job()).grid(row=1, column=3,padx=15, pady=5)
time_entry = tk.Entry(job_frame)
time_entry.insert(tk.END, "12:00:00")
time_entry.grid(row=1, column=2, padx=15, pady=5)
schedule_label = tk.Label(job_frame, text="Waiting for task...").grid(row=1, column=4, padx=15, pady=5)
                                        
tk.Label(job_frame, text="CLEAN: water only").grid(row=2, column=0, padx=15, pady=5)
tk.Button(job_frame, text="START", command=lambda: job_w_clean(task_on_1, task_off_1, task_on_2, task_off_2, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_5)).grid(row=2, column=1, padx=5, pady=5)#task for switching valves w/ appropraite delays for short cleaning (1 repeat)


tk.Label(job_frame, text="CLEAN: water + ethanol").grid(row=3, column=0, padx=15, pady=5)
tk.Button(job_frame, text="START",command=lambda: job_we_clean(task_on_1, task_off_1, task_on_2, task_off_2, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_5)).grid(row=3, column=1, padx=5, pady=5)#task for switching valves w/ appropraite delays for long cleaning (2 repeats)

# Create delay entry field
delay_label = tk.Label(job_frame, text="Delay (seconds):")
delay_label.grid(row=4,column=0, padx=5, pady=5)

delay_entry = tk.Entry(job_frame, width=10)
delay_entry.insert(tk.END, "0")  # Set default delay to 0 seconds
delay_entry.grid(row=4,column=1, padx=5, pady=5)


## quit frame
tk.Button(quit_frame, text="PRAY").grid(row=0,padx=5,pady=5) #box with a cheeky message
tk.Button(quit_frame, text="QUIT", command=lambda: job_quit(task_on_1, task_off_1, task_on_2, task_off_2, task_on_3, task_off_3, task_on_4, task_off_4, task_on_5, task_off_5, delay_entry,status_label_1, status_label_2, status_label_3, status_label_4, status_label_5)).grid(row=1,padx=5,pady=5) #in case it quits early, the function should switch valves to in reg_acsf and out waste and then window.destroy()

## status frame
# labels and buttons in frames
tk.Label(status_frame,text="Now flowing:").grid(row=0, column=0)
#where would be a default setting for inflow_status_label which will be updated with each swtich 
# if status_label_1 == tk.Label(valve_frame, text="CLOSED", fg="red"):
#     tk.Label(status_frame, text = "Drug ACSF").grid(row=0, column=1)
# else:
#     tk.Label(status_frame, text = "Reg. ACSF").grid(row=0, column=1)  


tk.Label(status_frame, text="Going to:").grid(row=0,column=2)
#where would be a default setting for outflow_status_label which will be updated with each swtich 

window.mainloop()



