#!/usr/bin/env python
import psutil
from crawlab import save_item
from db import save_item_to_kibana
# gives a single float value
cpu = psutil.cpu_percent()
# gives an object with many fields
#ram = psutil.virtual_memory()
# you can convert that object to a dictionary 
ram = dict(psutil.virtual_memory()._asdict())
# you can have the percentage of used RAM
# ram = psutil.virtual_memory().percent
#79.2
# you can calculate percentage of available memory
#psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
#20.8

hdd = psutil.disk_usage('/')

print (f"Total: {hdd.total / (2**30)} GiB")
print (f"Used: {hdd.used / (2**30)} GiB" )
print (f"Free: {hdd.free / (2**30)} GiB")



print(f"cpu: {cpu}")
print(f"ram: {ram}")
data = {
  "cpu": cpu,
  "ram": ram,
  "dict": {
    "Total": hdd.total / (2**30)},
    "Used": hdd.used / (2**30),
    "Free": hdd.free / (2**30),
    "Used Percent": hdd.used/hdd.total
  }
}
save_item(data)
save_item_to_kibana(data)
