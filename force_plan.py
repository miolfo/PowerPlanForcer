import sched, time
import os
import subprocess
from subprocess import check_output
import re

s = sched.scheduler(time.time, time.sleep)
list_command = "powercfg.exe -list"
exec_command = "powercfg.exe /setactive "
delay = 5
desired_plan_name="Balanced"
guid_pattern = re.compile("(:\ .*?\ )")
name_pattern = re.compile("(\([A-Za-z\ ]*\))")

def force_power_plan(sc): 
    plans = check_output(list_command).decode("utf-8")
    guid_results = guid_pattern.findall(plans)
    name_results = name_pattern.findall(plans)
    guids = []

    for guid_result in guid_results:
        guids.append(guid_result.replace(":", "").replace(" ", ""))

    index_of_desired = -1
    for index, name in enumerate(name_results):
        if desired_plan_name in name:
            index_of_desired = index
    
    guid_to_set = guids[index_of_desired]
    os.system(exec_command + guid_to_set)
    s.enter(delay, 1, force_power_plan, (s,))


s.enter(delay, 1, force_power_plan, (s,))
s.run()